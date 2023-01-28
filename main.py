import os
import shutil
import hashlib

from config_parser.main import parse_config
from file_operatios.main import get_config_absolute_path, get_related_files


def calculate_sha(path: str) -> str:
    hash_sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def main():
    config_path = get_config_absolute_path()
    config = parse_config(config_path)
    files_info = [(vm_config, get_related_files(config.source_path, vm_config.vm_id))
                  for vm_config in config.vm_configs]
    for (vm_info, files) in files_info:
        for file in files:
            origin_path = os.path.join(config.source_path, file)
            target_path = os.path.join(vm_info.target_path, file)
            original_sha = calculate_sha(origin_path)
            shutil.copy2(origin_path, target_path)
            copied_sha = calculate_sha(target_path)
            assert original_sha == copied_sha
    pass


if __name__ == '__main__':
    main()
