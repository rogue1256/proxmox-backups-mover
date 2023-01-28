import backup_mover_logger
import config_provider
import file_handler
import asyncio
import telegram_reporter

logger = backup_mover_logger.logger.get_logger()


def main():
    config = config_provider.get_config()
    logger.info("Starting collecting information about the files")
    files_info = [(vm_config, file_handler.filtering.get_related_files(config.source_path, vm_config.vm_id))
                  for vm_config in config.vm_configs]
    logger.info(f"Got the following VMs and corresponding files to process: {files_info}")
    file_copy_result = file_handler.copying.copy_vm_files(config, files_info)
    asyncio.run(telegram_reporter.result_reporter.report(file_copy_result))


if __name__ == '__main__':

    try:
        logger.debug("Trying to load a local default config")
        config_path = file_handler.file_paths.get_config_absolute_path()
        logger.debug("Initializing config")
        config_provider.initialize_config(config_path)
        main()
    except Exception as err:
        logger.exception(err)
        logger.fatal("Exception occurred")
