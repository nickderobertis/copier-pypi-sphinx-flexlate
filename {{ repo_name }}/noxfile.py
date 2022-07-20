import subprocess

import nox

nox.options.sessions = ["format", "strip", "lint", "test"]


@nox.session(python=False)
def format(session):
    if session.posargs:
        files = session.posargs
    else:
        files = ["."]

    if session.interactive:
        # When run as user, format the files in place
        _format_in_place(session, files)
    else:
        # When run from CI, fail the check if formatting is not correct
        session.run("isort", "--check-only", *files)
        session.run("black", "--check", *files)


@nox.session(python=False)
def format_files(session):
    if session.posargs:
        files = session.posargs
    else:
        files = ["."]

    _format_in_place(session, files)


def _format_in_place(session, files):
    session.run("isort", *files)
    session.run("black", *files)


@nox.session(python=False)
def lint(session):
    _setup_venv(session, "lint")

    def run_lint(*args):
        args_str = " ".join(args)
        _run(f"mvenv run lint -- {args_str}")

    run_lint(
        "flake8", "--count", "--select=E9,F63,F7,F82", "--show-source", "--statistics"
    )
    run_lint(
        "flake8",
        "--count",
        "--exit-zero",
        "--max-complexity=10",
        "--max-line-length=127",
        "--statistics",
    )
    run_lint("mypy")


@nox.session(python=False, name="strip")
def strip_imports(session):
    if session.posargs:
        files = session.posargs
    else:
        files = ["."]

    common_args = (
        "--remove-all-unused-imports",
        "--in-place",
        "--recursive",
        "--exclude=test*,__init__.py,venv*,build*,dist*,node_modules*",
        *files,
    )
    if session.interactive:
        # When run as user, strip unused imports and exit successfully
        session.run("autoflake", *common_args)
    else:
        # When run from CI, fail the check if stripping is not correct
        session.run("autoflake", "--check", *common_args)


@nox.session
def test(session):
    reqs_path = _tests_req_path(session)
    session.install(
        "-r", reqs_path, "--upgrade", "--upgrade-strategy", "eager"
    )
    session.install(".")
    session.run("pytest", *session.posargs)


@nox.session
def test_coverage(session):
    reqs_path = _tests_req_path(session)
    session.install(
        "-r", reqs_path, "--upgrade", "--upgrade-strategy", "eager"
    )
    session.install(".")
    session.run("pytest", "--cov=./", "--cov-report=xml")


@nox.session(python=False)
def docs(session):
    session.chdir("docsrc")
    session.run("make", "github")
    if session.interactive:
        session.run("bash", "./dev-server.sh")


def _tests_req_path(session) -> str:
    return session.run("mvenv", "run", "global", "python", "reqs_path.py", "test", external=True, silent=True).strip()


def _setup_venv(session, venv_name: str):
    if _venv_exists(venv_name):
        return
    session.run("mvenv", "sync", venv_name)


def _venv_exists(venv_name: str):
    exists_str = _run(
        f"mvenv info {venv_name} -i json | jq '.[0].exists'", stream=False
    ).strip()
    return exists_str == "true"


def _run(
    command: str,
    stream: bool = True,
) -> str:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
    )
    buffer = b""
    for c in iter(lambda: process.stdout.read(1), b""):  # type: ignore
        if stream:
            print(c.decode(), end="")
        buffer += c
    process.wait()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command)

    return buffer.decode()
