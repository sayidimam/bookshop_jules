import requests
import json
import urllib.parse
from django.conf import settings

class GreenwebClient:
    def __init__(self):
        self.token = getattr(settings, 'GREENWEB_TOKEN', '')
        self.base_url = "http://api.greenweb.com.bd/api.php"

    def send_sms(self, to, message):
        """
        Sends an SMS using the Greenweb API (JSON POST method).

        :param to: Recipient number (e.g., '017xxxxxxxx' or '+88017xxxxxxxx')
        :param message: The text message content
        :return: Response dictionary from the API
        """
        if not self.token:
            print("Greenweb Token not found in settings.")
            return None

        # Clean/Format the number (basic check)
        if not to.startswith('+88'):
            to = f"+88{to}" if to.startswith('01') else to

        payload = {
            "token": self.token,
            "smsdata": [
                {
                    "to": to,
                    "message": message
                }
            ]
        }

        try:
            response = requests.post(
                f"{self.base_url}?json",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload)
            )
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error sending SMS via Greenweb: {e}")
            return None
