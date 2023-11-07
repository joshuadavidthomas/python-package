import re
from pathlib import Path


def _search_and_replace(search_regex: str, replace: str):
    path = Path.cwd()

    complied_search = re.compile(search_regex, re.MULTILINE)

    for file in path.rglob("*"):
        if ".git" in file.parts or not file.is_file():
            continue

        try:
            text = file.read_text()
            new_text = complied_search.sub(replace, text)

            if new_text != text:
                file.write_text(new_text)
        except Exception as e:
            print(f"Error processing {file}: {e}")


def replace_versions(name: str, cc_versions: str, list_extra: str | None = None):
    versions = cc_versions.split(",")

    stringified_list = [f"{version}" for version in versions]
    if list_extra:
        stringified_list.append(list_extra)
    min = versions[0]
    max = versions[-1]

    _search_and_replace("{cookiecutter.%s_versions}" % name, f"{stringified_list}")
    _search_and_replace("{cookiecutter.%s_min_version}" % name, f"{min}")
    _search_and_replace("{cookiecutter.%s_max_version}" % name, f"{max}")


def replace_classifiers(name: str, classifier_template: str, cc_versions: str):
    versions = cc_versions.split(",")
    major_versions = set([version.split(".")[0] for version in versions])

    classifers_list = [
        f'\\1"{classifier_template} :: {version}",'
        for version in versions + list(major_versions)
    ]
    classifers_list.append(f'\\1"{classifier_template}",')

    if len(major_versions) == 1:
        classifers_list.append(
            f'\\1"{classifier_template} :: {major_versions.pop()} :: Only",'
        )

    sorted_list = sorted(classifers_list)

    _search_and_replace(
        r"(^\s*){cookiecutter\.%s_classifiers}" % name, "\n".join(sorted_list)
    )


def replace_test_versions(
    name: str,
    cc_versions: str,
):
    upper_name = name.upper()
    versions = cc_versions.split(",")

    stringified_list = [
        f'{upper_name}{version.replace(".","").upper()} = "{version}"'
        for version in versions
    ]
    variablified_list = [
        f"{upper_name}{version.replace('.','').upper()}" for version in versions
    ]
    default_version = sorted(stringified_list)[0].split("=")[0]
    default_variable = f"{default_version.replace('.','')}"

    template = "\n".join(stringified_list) + "\n"
    template += f"{upper_name}_VERSIONS = [{', '.join(variablified_list)}]\n"
    template += f"{upper_name}_DEFAULT = {default_variable}"

    _search_and_replace("{cookiecutter.test_%s_versions}" % name, f"{template}")


def replace_dependencies(cc_dependencies: str):
    dependencies = cc_dependencies.split(",")

    stringified_list = [f"{dependency}" for dependency in dependencies]

    _search_and_replace("{cookiecutter.dependencies}", f"{stringified_list}")


def main():
    replace_versions("python", "{{cookiecutter.python_versions}}")

    replace_classifiers(
        "python",
        "Programming Language :: Python",
        "{{cookiecutter.python_versions}}",
    )

    replace_test_versions("py", "{{cookiecutter.python_versions}}")

    replace_dependencies("{{cookiecutter.dependencies}}")


if __name__ == "__main__":
    main()
