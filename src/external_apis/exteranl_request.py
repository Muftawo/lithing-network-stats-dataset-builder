import json
import time
from typing import Any, Dict, Optional

import requests


class ExternalRequestService:
    """
    A service to perform HTTP/HTTPS requests with a specified timeout.
    """

    def __init__(self):
        # The maximum amount of time a request can go for. A custom timeout can be specified in the options dictionary.
        self.request_timeout: int = 180  # 3 minutes
        self.max_retries: int = 5
        # The base delay for exponential backoff (in seconds)
        self.base_delay: int = 2

    def request(
        self,
        options: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
        protocol_name: Optional[str] = "https",
    ) -> Dict[str, Any]:
        # Determine the protocol (http/https)
        url = f"{protocol_name}://{options['host']}{options['path']}"

        # If no timeout is set, use the default request timeout
        timeout = options.get("timeout", self.request_timeout)

        # Set up headers and request options
        request_kwargs = {
            "method": options["method"],
            "url": url,
            "headers": options.get("headers", {}),
            "timeout": timeout,
        }

        # Append params if provided
        if params:
            if options["method"] == "GET":
                request_kwargs["params"] = params
            else:
                request_kwargs["json"] = params

        # Perform the request with retry logic
        for attempt in range(self.max_retries):
            try:
                response = requests.request(**request_kwargs)

                # If the response is a 429 error, handle rate limiting
                if response.status_code == 429:
                    # Calculate the backoff time (exponential backoff)
                    backoff_time = self.base_delay * (2**attempt)
                    print(f"Rate limit hit. Retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                    continue  # Retry the request after the delay

                # Return the response if successful
                return {
                    "status_code": response.status_code,
                    "headers": response.headers,
                    "data": response.json() if response.content else None,
                }

            except requests.exceptions.RequestException as err:
                raise Exception(f"Error during request: {err}")

        # If max retries are exceeded, raise an error
        raise Exception("Exceeded maximum retries due to rate limiting.")

    def get_final_params(self, params: Optional[Dict[str, Any]]) -> Optional[str]:
        if params:
            return json.dumps(params)
        return None
