import os
import config_parser
import file_operatios
import sha_validator


def main():
    config_path = file_operatios.get_config_absolute_path()
    config = config_parser.parse_config(config_path)
    files_info = [(vm_config, file_operatios.get_related_files(config.source_path, vm_config.vm_id))
                  for vm_config in config.vm_configs]
    for (vm_info, files) in files_info:
        for file in files:
            origin_path = os.path.join(config.source_path, file)
            target_path = os.path.join(vm_info.target_path, file)
            file_operatios.copy_files(origin_path, target_path)
            if not sha_validator.validate_files(origin_path, target_path):
                raise ValueError()


if __name__ == '__main__':
    main()
