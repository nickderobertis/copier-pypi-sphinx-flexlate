import argparse
from pathlib import Path

import multivenv


def main():
    # Use argparse to accept zero or more arguments containing venv name
    parser = argparse.ArgumentParser(description="Get requirements out path for a venv")
    parser.add_argument("venv_names", nargs="*", help="Name of venv")
    args = parser.parse_args()
    venv_names = args.venv_names or None

    config_path = Path("mvenv.yaml")
    config_class = multivenv.info.model_cls  # type: ignore
    config = config_class.load(config_path)
    venvs = config.venvs

    info = multivenv.info(venv_names, venvs=venvs, quiet=True)
    out_paths = [info.discovered_requirements.out_path for info in info]
    out_str = ", ".join(str(path) for path in out_paths)
    print(out_str)


if __name__ == "__main__":
    main()
