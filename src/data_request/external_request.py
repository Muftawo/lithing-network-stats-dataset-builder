import logging
import time
from typing import Any, Dict, Optional

import requests


class ExternalRequest:
    def __init__(self):
        self.request_timeout: int = 180  # 3 minutes
        self.max_retries: int = 5
        self.base_delay: int = 2

    def request(
        self,
        options: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"https://{options['host']}{options['path']}"
        timeout = options.get("timeout", self.request_timeout)

        request_kwargs = {
            "method": options["method"],
            "url": url,
            "headers": options.get("headers", {}),
            "timeout": timeout,
        }

        if options["method"] in {"POST", "PUT", "PATCH"}:
            request_kwargs["json"] = params
        elif options["method"] == "GET" and params:
            request_kwargs["params"] = params

        for attempt in range(self.max_retries):
            try:
                response = requests.request(**request_kwargs)

                if response.status_code == 429:  # rate limit error code
                    backoff_time = self.base_delay * (2**attempt)
                    logging.info(
                        f"Rate limit hit. Retrying in {backoff_time} seconds..."
                    )
                    time.sleep(backoff_time)
                    continue

                return {
                    "status_code": response.status_code,
                    "headers": response.headers,
                    "data": response.json() if response.content else None,
                }

            except requests.exceptions.Timeout as err:
                raise Exception(f"Request timed out: {err}")
            except requests.exceptions.ConnectionError as err:
                raise Exception(f"Connection error occurred: {err}")
            except requests.exceptions.RequestException as err:
                raise Exception(f"Error during request: {err}")

        raise Exception("Exceeded maximum retries due to rate limiting.")
