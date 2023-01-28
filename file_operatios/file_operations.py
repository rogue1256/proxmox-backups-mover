import os
import shutil

from backup_mover_logger.logger import get_logger

logger = get_logger()


def get_config_absolute_path() -> os.path:
    return os.path.join(os.getcwd(), "config.json")


def get_related_files(source_path: os.path, vm_id: int) -> list[str]:
    files = os.listdir(source_path)
    related_files = []
    for name in files:
        if os.path.isfile(os.path.join(source_path, name)) and f"qemu-{vm_id}-" in name:
            related_files.append(name)

    return related_files


def copy_files(source_path: os.path, target_path: os.path):
    if not os.path.isfile(source_path):
        logger.error(f"Source path is not a file {source_path}")
        raise ValueError()

    shutil.copy2(source_path, target_path)
