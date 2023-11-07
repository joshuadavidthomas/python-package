from __future__ import annotations

import os
from pathlib import Path

import nox

{cookiecutter.test_py_versions}


@nox.session(python=PY_VERSIONS)
def tests(session):
    session.install(".[dev]")

    session.run("python", "-m", "pytest")


@nox.session
def coverage(session):
    session.install(".[dev]")
    session.run("python", "-m", "pytest", "--cov={{cookiecutter.package_name}}")

    try:
        summary = os.environ["GITHUB_STEP_SUMMARY"]
        with Path(summary).open("a") as output_buffer:
            output_buffer.write("")
            output_buffer.write("### Coverage\n\n")
            output_buffer.flush()
            session.run(
                "python",
                "-m",
                "coverage",
                "report",
                "--skip-covered",
                "--skip-empty",
                "--format=markdown",
                stdout=output_buffer,
            )
    except KeyError:
        session.run(
            "python", "-m", "coverage", "html", "--skip-covered", "--skip-empty"
        )

    session.run("python", "-m", "coverage", "report")


@nox.session
def lint(session):
    session.install(".[lint]")
    session.run("python", "-m", "pre_commit", "run", "--all-files")


@nox.session
def mypy(session):
    session.install(".[dev]")
    session.run("python", "-m", "mypy", ".")
