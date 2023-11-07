"""
{{ cookiecutter.update({ "email": cookiecutter.email | trim }) }}
"""

package_name = "{{ cookiecutter.package_name }}"
if hasattr(package_name, "isidentifier"):
    assert (
        package_name.isidentifier()
    ), f"'{package_name}' project slug is not a valid Python identifier."

assert (
    package_name == package_name.lower()
), f"'{package_name}' project slug should be all lowercase"

assert (
    "\\" not in "{{ cookiecutter.author_name }}"
), "Don't include backslashes in author name."
