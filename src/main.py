import logging
import sys

from dataset_builder.builder import DatasetBuilderService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/logs.log"),  
        # logging.StreamHandler(sys.stdout),  # Log to the console
    ],
)

logger = logging.getLogger(__name__)

logger.info("BITCOIN LIGHTNING NETWORK STATS DATASET BUILDER")
logger.info(" ")


def main():
    try:
        dataset_builder = DatasetBuilderService()
        dataset_builder.sync()
        logger.info("\nThe dataset has been synced successfully")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
