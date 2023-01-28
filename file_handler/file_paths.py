import os


def get_config_absolute_path() -> os.path:
    return os.path.join(os.getcwd(), "config.json")
