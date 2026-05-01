# akn_sdk/transport/http_client.py

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HTTPClient:

    def __init__(self, base_url, token=None, timeout=10, retries=5):
        self.base_url = base_url
        self.token = token
        self.timeout = timeout

        self.session = requests.Session()

        retry_strategy = Retry(
            total=retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def set_token(self, token: str):
        self.token = token

    def post(self, path, json_data):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        print("📤 Sending to Gateway:")
        print(json_data)

        response = self.session.post(
            f"{self.base_url}{path}",
            json=json_data,
            headers=headers,
            timeout=self.timeout,
        )

        if not response.ok:
            print("❌ Gateway Error Response:")
            print(response.status_code)
            print(response.text)
            response.raise_for_status()

        return response.json()