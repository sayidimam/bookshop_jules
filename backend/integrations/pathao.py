import requests
from rest_framework.exceptions import APIException
from datetime import datetime, timedelta

class PathaoClient:
    def __init__(self, account):
        """
        Initialize with a specific CourierAccount object instead of global settings.
        """
        self.account = account
        self.base_url = "https://courier-api-sandbox.pathao.com" # Should ideally come from account config or env
        # For production use: https://api-hermes.pathao.com

        self.client_id = account.client_id
        self.client_secret = account.secret_key
        self.username = account.username
        self.password = account.password

        self.access_token = None
        self.token_expiry = None

    def _get_headers(self):
        if not self.access_token or datetime.now() >= self.token_expiry:
            self._authenticate()
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def _authenticate(self):
        url = f"{self.base_url}/aladdin/api/v1/issue-token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "password",
            "username": self.username,
            "password": self.password
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            self.token_expiry = datetime.now() + timedelta(seconds=data['expires_in'] - 60)
        else:
            raise APIException(f"Pathao Auth Failed: {response.text}")

    def create_order(self, order_data):
        url = f"{self.base_url}/aladdin/api/v1/orders"
        response = requests.post(url, json=order_data, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        raise APIException(f"Pathao Create Order Failed: {response.text}")

    # ... other methods (get_cities, etc.) remain similar but use self._get_headers()
