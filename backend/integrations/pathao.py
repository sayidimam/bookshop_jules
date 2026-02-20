import requests
from django.conf import settings
from rest_framework.exceptions import APIException
from datetime import datetime, timedelta

class PathaoClient:
    def __init__(self):
        self.base_url = settings.PATHAO['BASE_URL']
        self.client_id = settings.PATHAO['CLIENT_ID']
        self.client_secret = settings.PATHAO['CLIENT_SECRET']
        self.username = settings.PATHAO['USERNAME']
        self.password = settings.PATHAO['PASSWORD']
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

    def create_store(self, store_data):
        url = f"{self.base_url}/aladdin/api/v1/stores"
        response = requests.post(url, json=store_data, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        raise APIException(f"Pathao Create Store Failed: {response.text}")

    def create_order(self, order_data):
        """
        Create a new order in Pathao
        Payload: {
            "store_id": 123,
            "merchant_order_id": "ORD-101",
            "recipient_name": "John Doe",
            "recipient_phone": "017...",
            "recipient_address": "Dhaka...",
            "recipient_city": 1,
            "recipient_zone": 1,
            "delivery_type": 48,
            "item_type": 2,
            "item_quantity": 1,
            "item_weight": 0.5,
            "amount_to_collect": 500
        }
        """
        url = f"{self.base_url}/aladdin/api/v1/orders"
        response = requests.post(url, json=order_data, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        raise APIException(f"Pathao Create Order Failed: {response.text}")

    def calculate_price(self, price_data):
        url = f"{self.base_url}/aladdin/api/v1/merchant/price-plan"
        response = requests.post(url, json=price_data, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        raise APIException(f"Pathao Price Calc Failed: {response.text}")

    def get_cities(self):
        url = f"{self.base_url}/aladdin/api/v1/city-list"
        response = requests.get(url, headers=self._get_headers())
        return response.json()

    def get_zones(self, city_id):
        url = f"{self.base_url}/aladdin/api/v1/cities/{city_id}/zone-list"
        response = requests.get(url, headers=self._get_headers())
        return response.json()

    def get_areas(self, zone_id):
        url = f"{self.base_url}/aladdin/api/v1/zones/{zone_id}/area-list"
        response = requests.get(url, headers=self._get_headers())
        return response.json()
