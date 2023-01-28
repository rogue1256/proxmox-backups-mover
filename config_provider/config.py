import json
import os

from config_provider.models import BackupInfo, BackupConfig
import backup_mover_logger

config = None
logger = backup_mover_logger.logger.get_logger()


def initialize_config(path: str | None = None):
    global config
    if path is None:
        logger.debug("Got an empty string. Defaulting to a local config.json file.")
        path = os.path.join(os.getcwd(), "config.json")
    else:
        logger.debug(f"Using the path provided {path}")

    try:
        logger.debug(f"Trying to read the config file at {path}")
        with open(path, 'r') as config_file:
            json_config: dict = json.load(config_file)
            logger.debug(f"Got the following json: {json_config}")
            source_path = os.path.join(*json_config.get("backup_source_path"))
            target_path = os.path.join(*json_config.get("backup_target_path"))
            vm_list: list[BackupInfo] = []
            for vm in json_config.get("backup_configs"):
                friendly_name = vm.get("friendly_name")
                vm_id = vm.get("vm_id")
                vm_target_path = os.path.join(target_path, *vm.get("target_path_in_cloud"))
                vm_list.append(BackupInfo(friendly_name, vm_id, vm_target_path))

            config = BackupConfig(source_path, vm_list, json_config.get("log_level"))
    except Exception as err:
        logger.exception(err)
        logger.fatal("Could not load the config file")


def get_config():
    global config
    if config is None:
        initialize_config()

    return config
