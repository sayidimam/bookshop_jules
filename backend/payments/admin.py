from django.contrib import admin
from .models import PaymentMethod, MobilePaymentLog, Transaction, Coupon, Wallet, WalletTransaction
from .models_parsing import SmsParsingRule
from .admin_parsing import SmsParsingRuleAdmin

admin.site.register(PaymentMethod)
admin.site.register(MobilePaymentLog)
admin.site.register(Transaction)
admin.site.register(Coupon)
admin.site.register(Wallet)
admin.site.register(WalletTransaction)
# SmsParsingRule is registered via decorator in admin_parsing.py, but we need to ensure it's imported
