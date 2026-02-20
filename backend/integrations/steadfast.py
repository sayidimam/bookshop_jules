import requests
from django.conf import settings
from rest_framework.exceptions import APIException

class SteadfastClient:
    def __init__(self):
        self.api_key = settings.STEADFAST['API_KEY']
        self.secret_key = settings.STEADFAST['SECRET_KEY']
        self.base_url = settings.STEADFAST['BASE_URL']
        self.headers = {
            'Api-Key': self.api_key,
            'Secret-Key': self.secret_key,
            'Content-Type': 'application/json'
        }

    def create_order(self, order_data):
        """
        Create a new consignment in Steadfast

        Payload:
        {
            "invoice": "unique_invoice_id",
            "recipient_name": "John Doe",
            "recipient_phone": "017...",
            "recipient_address": "Address...",
            "cod_amount": 1000,
            "note": "Deliver by 3PM"
        }
        """
        url = f"{self.base_url}/create_order"
        response = requests.post(url, json=order_data, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise APIException(f"Steadfast Error: {response.text}")

    def check_status_by_invoice(self, invoice_id):
        url = f"{self.base_url}/status_by_invoice/{invoice_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def check_status_by_tracking_code(self, tracking_code):
        url = f"{self.base_url}/status_by_trackingcode/{tracking_code}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_current_balance(self):
        url = f"{self.base_url}/get_balance"
        response = requests.get(url, headers=self.headers)
        return response.json()
