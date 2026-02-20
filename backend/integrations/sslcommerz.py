from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
import uuid

class SSLCommerzClient:
    def __init__(self):
        self.settings = {
            'store_id': settings.SSLCOMMERZ['STORE_ID'],
            'store_pass': settings.SSLCOMMERZ['STORE_PASS'],
            'issandbox': settings.SSLCOMMERZ['IS_SANDBOX']
        }
        self.sslcz = SSLCOMMERZ(self.settings)

    def initiate_payment(self, order, user):
        post_body = {}
        post_body['total_amount'] = order.total_amount
        post_body['currency'] = "BDT"
        post_body['tran_id'] = f"TRX-{uuid.uuid4()}" # Generate unique TRX ID
        post_body['success_url'] = "http://localhost:8000/api/payment/success/"
        post_body['fail_url'] = "http://localhost:8000/api/payment/fail/"
        post_body['cancel_url'] = "http://localhost:8000/api/payment/cancel/"
        post_body['emi_option'] = 0

        post_body['cus_name'] = user.full_name or "Guest"
        post_body['cus_email'] = user.email or "guest@example.com"
        post_body['cus_phone'] = user.phone_number
        post_body['cus_add1'] = order.shipping_address
        post_body['cus_city'] = "Dhaka" # Should come from order
        post_body['cus_country'] = "Bangladesh"

        post_body['shipping_method'] = "NO"
        post_body['product_name'] = "Books"
        post_body['product_category'] = "Books"
        post_body['product_profile'] = "general"

        response = self.sslcz.createSession(post_body)
        return response # {'status': 'SUCCESS', 'GatewayPageURL': '...'}

    def validate_payment(self, post_data):
        return self.sslcz.validationTransactionOrder(post_data)
