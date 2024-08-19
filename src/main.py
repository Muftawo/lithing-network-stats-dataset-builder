import logging
import os
import sys

from dataset_builder.builder import DatasetBuilder

# Constants for exit codes
SUCCESS = 0
FAILURE = 1

# Configurable logging level and file path
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/DatasetBuilderLogger.log")


def configure_logging():
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL, logging.INFO),
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(LOG_FILE_PATH),
                # logging.StreamHandler(sys.stdout),  # Uncomment for console logging
            ],
        )


def run_sync(dataset_builder, logger):
    try:
        dataset_builder.sync()
        logger.info("The dataset has been synced successfully")
        return SUCCESS
    except Exception as e:
        logger.exception("An error occurred during dataset sync:")
        return FAILURE


def main():
    configure_logging()
    logger = logging.getLogger("DatasetBuilderLogger")

    logger.info("BITCOIN LIGHTNING NETWORK STATS DATASET BUILDER")
    logger.info(" ")

    dataset_builder = DatasetBuilder()

    # Run the sync and return the exit code
    exit_code = run_sync(dataset_builder, logger)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
