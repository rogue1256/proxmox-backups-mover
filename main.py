import os
import shutil

from config_parser.main import parse_config
from file_operatios.main import get_config_absolute_path, get_related_files


def main():
    config_path = get_config_absolute_path()
    config = parse_config(config_path)
    files_info = [(vm_config, get_related_files(config.source_path, vm_config.vm_id))
                  for vm_config in config.vm_configs]
    for (vm_info, files) in files_info:
        for file in files:
            origin = os.path.join(config.source_path, file)
            target_path = os.path.join(vm_info.target_path, file)
            shutil.copy2(origin, target_path)
    pass


if __name__ == '__main__':
    main()
