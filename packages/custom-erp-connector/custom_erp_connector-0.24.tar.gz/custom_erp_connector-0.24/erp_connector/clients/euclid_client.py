import json
import os
import uuid

import requests
from erp_connector.utils.retryable_session import RetryableSession
from erp_connector.utils.custlogging import LoggerProvider

logger = LoggerProvider().get_logger(os.path.basename(__file__))


class EuclidClient:

    def __init__(self):
        self.base_url = f"https://app-dev-http.clear.in"
        self.table_id = "13e2d644-9feb-451a-a310-901f5f1f94a8"

    def post_events(self, request_data):
        session = RetryableSession()
        url = f"{self.base_url}/api/analytics/events"
        headers = {
            "accept": "*/*",
            'Content-Type': 'application/json'
        }
        request_payload = [
            {
                "analyticsId": str(uuid.uuid4()),
                "tableId": self.table_id,
                "data": json.dumps(request_data)
            }
        ]
        payload = json.dumps(request_payload)

        try:
            response = session.post(url, headers=headers, data=payload, timeout=45)
            response.raise_for_status()
            response_data = response.json()
            return response_data
        except requests.exceptions.HTTPError as http_err:
            raise Exception(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            raise Exception(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            raise Exception(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            raise Exception(f"An error occurred: {req_err}")
