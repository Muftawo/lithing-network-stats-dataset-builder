import logging
from typing import Any, Dict, List

import requests

from .exteranl_request import ExternalRequestService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MempoolSpaceService:
    def __init__(self):
        # Mempool.space's Request Options Skeleton
        self.request_options = {
            "host": "mempool.space",
            "path": "",
            "method": "GET",
            "headers": {"Content-Type": "application/json"},
        }

        self._external_request = ExternalRequestService()

    def get_lightning_network_stats(self) -> List[Dict[str, Any]]:
        # Send the request
        response = self._external_request.request(
            {**self.request_options, "path": "/api/v1/lightning/statistics/3y"}
        )
        # Validate the response
        self.validate_request_response(response)

        # Parse the JSON response data
        data = response.json()

        # Validate the response's data
        if not isinstance(data, list):
            logger.error("Invalid list of stat records received: %s", type(data))
            raise ValueError(
                f"Mempool.space's API returned an invalid list of stat records. Received: {type(data)}"
            )
        if not data:
            logger.warning(
                "Mempool.space's API returned an empty list of stat records."
            )
            raise ValueError(
                "Mempool.space's API returned an empty list of stat records."
            )

        # Return the validated data
        return data

    def validate_request_response(self, response: requests.Response) -> None:
        # Ensure it is a valid response object
        if not response or not isinstance(response, requests.Response):
            logger.error("Invalid response object received: %s", response)
            raise ValueError("Mempool.space's API returned an invalid response object.")

        # Ensure the status code is valid
        if response.status_code != 200:
            logger.error(
                "Invalid HTTP response code. Expected: 200, Received: %s",
                response.status_code,
            )
            raise ValueError(
                f"Mempool.space's API returned an invalid HTTP response code. "
                f"Expected: 200, Received: {response.status_code}"
            )
