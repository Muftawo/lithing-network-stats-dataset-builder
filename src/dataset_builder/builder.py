import csv
import logging
import os
from typing import Dict, List

from data_request.mempool_space import MempoolSpaceApiRequest

CSV_HEADER = [
    "added",
    "channel_count",
    "total_capacity",
    "tor_nodes",
    "clearnet_nodes",
    "unannounced_nodes",
    "clearnet_tor_nodes",
]


class DatasetBuilder:
    def __init__(
        self,
        dataset_path: str = "data/dataset.csv",
    ):
        self.dataset_path = dataset_path
        self._mempool_space = MempoolSpaceApiRequest()
        self.initialize_dataset_file()

    def initialize_dataset_file(self) -> None:
        if not os.path.exists(self.dataset_path):
            os.makedirs(os.path.dirname(self.dataset_path), exist_ok=True)
            self._write_csv_header()

    def _write_csv_header(self) -> None:
        try:
            with open(self.dataset_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(CSV_HEADER)
            logging.info("Initialized new dataset file with headers.")
        except IOError as e:
            logging.error(f"Failed to write CSV header: {e}")

    def load_latest_timestamp(self) -> int:
        if not os.path.exists(self.dataset_path):
            return 0
        try:
            with open(self.dataset_path, mode="r") as file:
                lines = file.readlines()
                if len(lines) <= 1:
                    return 0
                latest_timestamp = int(lines[-1].split(",")[0])
                logging.debug(f"Loaded latest timestamp: {latest_timestamp}")
                return latest_timestamp
        except IOError as e:
            logging.error(f"Failed to load latest timestamp: {e}")
            return 0

    def update_dataset_file(self, records: List[Dict[str, int]]) -> None:
        try:
            with open(self.dataset_path, mode="a", newline="") as file:
                writer = csv.writer(file)
                for record in records:
                    writer.writerow(
                        [
                            record["added"],
                            record["channel_count"],
                            record["total_capacity"],
                            record["tor_nodes"],
                            record["clearnet_nodes"],
                            record["unannounced_nodes"],
                            record["clearnet_tor_nodes"],
                        ]
                    )
            logging.info(f"Updated dataset file with {len(records)} new records.")
        except IOError as e:
            logging.error(f"Failed to update dataset file: {e}")

    def get_new_records(self, latest_timestamp: int) -> List[Dict[str, int]]:
        records = self._mempool_space.get_lightning_network_stats()
        new_records = [
            record for record in records if record["added"] > latest_timestamp
        ]
        logging.info(f"Retrieved {len(new_records)} new records from Mempool.space.")
        return new_records

    def sync(self) -> None:
        latest_timestamp = self.load_latest_timestamp()
        new_records = self.get_new_records(latest_timestamp)
        if new_records:
            self.update_dataset_file(new_records)
        else:
            logging.info("No new records to add.")
