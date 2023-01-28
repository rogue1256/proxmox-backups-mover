import os
import shutil

import file_handler
import sha_validator
from backup_mover_logger.logger import get_logger
from config_provider.models import BackupMoverConfig, VmInfo
from file_handler.models import FailReason, VmFilesCopyResult

logger = get_logger()


def copy_files(source_path: os.path, target_path: os.path):
    if not os.path.isfile(source_path):
        logger.error(f"Source path is not a file {source_path}")
        raise ValueError()

    shutil.copy2(source_path, target_path)


def copy_vm_files(config: BackupMoverConfig, files_info: [(VmInfo, [str])]) -> [VmFilesCopyResult]:
    result: [VmFilesCopyResult] = []
    for (vm_info, files) in files_info:
        copied_files: [(str, str)] = []
        failed_files: [(str, FailReason)] = []
        for file in files:
            origin_path = os.path.join(config.source_path, file)
            target_path = os.path.join(vm_info.target_path, file)
            logger.debug(f"Trying to copy {origin_path} to {target_path}")
            try:
                file_handler.copying.copy_files(origin_path, target_path)
                logger.info("Successfully copied the file.")
                logger.debug("Validating files SHA256 to confirm validity of the backup")
                file1_hash = sha_validator.calculate_sha256(origin_path)
                file2_hash = sha_validator.calculate_sha256(target_path)
                if file1_hash != file2_hash:
                    logger.error(
                        f"Hashes {file2_hash} and {file2_hash} are different for files {origin_path} and {target_path}")
                    failed_files.append((origin_path, FailReason.DifferentSha256))
                else:
                    copied_files.append((origin_path, target_path))
                    logger.info(f"Successfully copied file {origin_path} to {target_path} with valid hashes")
            except ValueError as err:
                logger.error(f"Could not correctly finish copying file {origin_path} to {target_path}")
                logger.exception(err)
                failed_files.append((origin_path, FailReason.CopyFailed))
            finally:
                result.append(VmFilesCopyResult(vm_info, copied_files, failed_files))
    return result
