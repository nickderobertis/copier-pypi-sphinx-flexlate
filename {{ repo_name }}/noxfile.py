import nox

nox.options.sessions = ["format", "lint", "test"]


@nox.session(python=False)
def format(session):
    if session.interactive:
        # When run as user, format the files in place
        session.run("isort", ".")
        session.run("black", ".")
    else:
        # When run from CI, fail the check if formatting is not correct
        session.run("isort", "--check-only", ".")
        session.run("black", "--check", ".")


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
    session.install(
        "-r", "test-requirements.txt", "--upgrade", "--upgrade-strategy", "eager"
    )
    session.install(".")
    session.run("pytest")


@nox.session
def test_coverage(session):
    session.install(
        "-r", "test-requirements.txt", "--upgrade", "--upgrade-strategy", "eager"
    )
    session.install(".")
    session.run("pytest", "--cov=./", "--cov-report=xml")


@nox.session(python=False)
def docs(session):
    session.chdir("docsrc")
    session.run("make", "github")
    if session.interactive:
        session.run("ls", "-l")
        session.run("bash", "./dev-server.sh")
