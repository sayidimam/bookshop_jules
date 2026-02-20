import requests
from rest_framework.exceptions import APIException

class SteadfastClient:
    def __init__(self, account):
        """
        Initialize with a specific CourierAccount object.
        """
        self.account = account
        self.api_key = account.api_key
        self.secret_key = account.secret_key
        self.base_url = "https://portal.packzy.com/api/v1" # Can be configurable

        self.headers = {
            'Api-Key': self.api_key,
            'Secret-Key': self.secret_key,
            'Content-Type': 'application/json'
        }

    def create_order(self, order_data):
        url = f"{self.base_url}/create_order"
        response = requests.post(url, json=order_data, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise APIException(f"Steadfast Error: {response.text}")

    def check_status_by_tracking_code(self, tracking_code):
        url = f"{self.base_url}/status_by_trackingcode/{tracking_code}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def check_discrepancy(self, consignment, actual_data):
        """
        Checks if the courier's reported charge/COD matches our records.
        """
        discrepancies = []

        # Check COD Mismatch
        if actual_data.get('cod_amount') != float(consignment.expected_cod):
            discrepancies.append({
                'reason': 'COD_MISMATCH',
                'claimed': actual_data.get('cod_amount'),
                'expected': consignment.expected_cod
            })

        return discrepancies
