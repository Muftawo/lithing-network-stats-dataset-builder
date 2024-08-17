import csv
import os
import time
from typing import Dict, List, Tuple

from external_apis.mempool_space import MempoolSpaceService


class DatasetBuilderService:
    def __init__(self):

        self.dataset_path = "data/dataset.csv"

        self._mempool_space = MempoolSpaceService()

        self.initialize_dataset_file()

    def sync(self):
        latest_timestamp, raw_dataset = self.load_dataset_file()

        new_records = self.get_dataset_items(latest_timestamp)

        if new_records:
            # If the file is empty, add the heading
            if not raw_dataset:
                raw_dataset = ",".join(new_records[0].keys())

            # Add the new records to the raw dataset
            raw_dataset += "".join(
                f"\n{','.join(map(str, record.values()))}" for record in new_records
            )

            # Update the dataset file
            self.update_dataset_file(raw_dataset)
        else:
            print("No new records")

    def get_dataset_items(self, latest_timestamp: int) -> List[Dict[str, any]]:
        # Retrieve raw records
        records = self._mempool_space.get_lightning_network_stats()

        # Sort the records in ascending order by timestamp
        records.sort(key=lambda x: x["added"])

        # Convert timestamps to milliseconds and filter new records
        return [
            {**record, "added": record["added"] * 1000}
            for record in records
            if record["added"] * 1000 > latest_timestamp
        ]

    def initialize_dataset_file(self):
        # Check if the dataset file exists
        if not self.path_exists(self.dataset_path):
            # Create the directory if it doesn't exist
            dir_name = os.path.dirname(self.dataset_path)
            if not self.path_exists(dir_name):
                os.makedirs(dir_name)

            # Create an empty CSV file
            self.update_dataset_file("")

    def update_dataset_file(self, new_data_state: str):
        with open(self.dataset_path, "w", encoding="utf-8") as file:
            file.write(new_data_state)

    def path_exists(self, file_or_dir_path: str) -> bool:
        return os.path.exists(file_or_dir_path)

    def load_dataset_file(self) -> Tuple[int, str]:
        if not self.path_exists(self.dataset_path):
            return 0, ""

        with open(self.dataset_path, "r", encoding="utf-8") as file:
            raw_dataset = file.read()

        if raw_dataset:
            latest_timestamp = int(raw_dataset.strip().split("\n")[-1].split(",")[0])
            return latest_timestamp, raw_dataset
        else:
            return 0, ""
