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

    def create_session(self, order_data, success_url, fail_url, cancel_url):
        post_body = {
            'total_amount': order_data['amount'],
            'currency': "BDT",
            'tran_id': order_data['trx_id'],
            'success_url': success_url,
            'fail_url': fail_url,
            'cancel_url': cancel_url,
            'emi_option': 0,
            'cus_name': order_data['customer_name'],
            'cus_email': order_data['customer_email'],
            'cus_phone': order_data['customer_phone'],
            'cus_add1': order_data['address'],
            'cus_city': order_data.get('city', 'Dhaka'),
            'cus_country': "Bangladesh",
            'shipping_method': "NO",
            'multi_card_name': "",
            'num_of_item': 1,
            'product_name': "Books",
            'product_category': "Books",
            'product_profile': "general"
        }

        response = self.sslcz.createSession(post_body)
        return response

    def validate_ipn(self, post_body):
        return self.sslcz.hash_validate_ipn(post_body)

    def validate_transaction(self, val_id):
        return self.sslcz.validationTransactionOrder(val_id)

    def init_refund(self, bank_tran_id, amount, remarks):
        return self.sslcz.init_refund(bank_tran_id, amount, remarks)
