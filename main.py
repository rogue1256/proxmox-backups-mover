from enum import Enum

import backup_mover_logger
import os
import config_provider
import file_operatios
import sha_validator

logger = backup_mover_logger.logger.get_logger()


class FailReason(Enum):
    Unknown = 0
    DifferentSha256 = 1
    CopyFailed = 2


def main():
    logger.debug("Trying to load a local default config")
    config_path = file_operatios.get_config_absolute_path()
    logger.debug("Initializing config")
    config_provider.initialize_config(config_path)
    config = config_provider.get_config()

    logger.info("Starting collecting information about the files")
    files_info = [(vm_config, file_operatios.get_related_files(config.source_path, vm_config.vm_id))
                  for vm_config in config.vm_configs]
    logger.info(f"Got the following VMs and corresponding files to process: {files_info}")
    failed_files: [(str, FailReason)] = []
    for (vm_info, files) in files_info:
        for file in files:
            origin_path = os.path.join(config.source_path, file)
            target_path = os.path.join(vm_info.target_path, file)
            logger.debug(f"Trying to copy {origin_path} to {target_path}")
            try:
                file_operatios.copy_files(origin_path, target_path)
                logger.info("Successfully copied the file.")
                logger.debug("Validating files SHA256 to confirm validity of the backup")
                file1_hash = sha_validator.calculate_sha256(origin_path)
                file2_hash = sha_validator.calculate_sha256(target_path)
                if file1_hash != file2_hash:
                    logger.error(
                        f"Hashes {file2_hash} and {file2_hash} are different for files {origin_path} and {target_path}")
                    failed_files.append((origin_path, FailReason.DifferentSha256))
            except ValueError as err:
                logger.error(f"Could not correctly finish copying file {origin_path} to {target_path}")
                logger.exception(err)
                failed_files.append((origin_path, FailReason.CopyFailed))
    # todo: report errors to telegram


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        logger.exception(err)
        logger.fatal("Exception occurred")
