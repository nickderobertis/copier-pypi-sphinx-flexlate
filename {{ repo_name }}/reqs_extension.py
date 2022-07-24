from pathlib import Path

import multivenv


def main():
    config_path = Path("mvenv.yaml")
    config_class = multivenv.info.model_cls  # type: ignore
    config = config_class.load(config_path)
    venvs = config.venvs

    info = multivenv.info(None, venvs=venvs, quiet=True)
    print(info.system.file_extension)


if __name__ == "__main__":
    main()
