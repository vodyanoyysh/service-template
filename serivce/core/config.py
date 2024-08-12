from pathlib import Path

from configmap import Config


def get_config(config_file: str) -> dict:
    cfg = Config(f"{Path.cwd()}", [config_file])
    cfg.load_config()
    return getattr(cfg, config_file.split(".")[0])
