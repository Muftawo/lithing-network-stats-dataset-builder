import logging
from typing import Any, Dict, List

from .external_request import ExternalRequest

API_PATH = "/api/v1/lightning/statistics/3y"  # Get stats for the past 3 years


class MempoolSpaceApiRequest:
    def __init__(self):
        self.request_options = {
            "host": "mempool.space",
            "path": "",
            "method": "GET",
            "headers": {"Content-Type": "application/json"},
        }
        self._external_request = ExternalRequest()

    def get_lightning_network_stats(self) -> List[Dict[str, Any]]:
        try:
            # Assume the request returns a dict containing 'status_code', 'headers', and 'data'
            response = self._external_request.request(
                {**self.request_options, "path": API_PATH}
            )
            self.validate_request_response(response)

            data = response["data"]  # Access the actual data part of the response
            self.validate_data(data)

            return data
        except ValueError as e:
            logging.error("Data validation error: %s", e)
            raise
        except Exception:
            logging.exception("Unexpected error occurred while retrieving stats")
            raise

    def validate_request_response(self, response: Dict[str, Any]) -> None:
        # Validate using the 'status_code' from the response dictionary
        if response.get("status_code") != 200:
            logging.error(
                "Unexpected HTTP response code. Expected: 200, Received: %s",
                response.get("status_code"),
            )
            raise ValueError(
                f"Unexpected HTTP response code: {response.get('status_code')}"
            )

    def validate_data(self, data: Any) -> None:
        if not isinstance(data, list):
            logging.error("Invalid data type received: %s", type(data))
            raise ValueError(f"Invalid data type received: {type(data)}")

        if not data:
            logging.warning("Received an empty list of stat records.")
            raise ValueError("Received an empty list of stat records.")
