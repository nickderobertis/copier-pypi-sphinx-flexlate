import nox


@nox.session(python=False)
def format(session):
    session.run("isort", ".")
    session.run("black", ".")


@nox.session(python=False)
def lint(session):
    session.run(
        "flake8", "--count", "--select=E9,F63,F7,F82", "--show-source", "--statistics"
    )
    session.run(
        "flake8",
        "--count",
        "--exit-zero",
        "--max-complexity=10",
        "--max-line-length=127",
        "--statistics",
    )
    session.run("mypy")


@nox.session
def test(session):
    session.install("-r", "test-requirements.txt")
    session.install(".")
    session.run("pytest")
