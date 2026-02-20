from django.db import models
from django.conf import settings
from orders.models import Order
from django.utils.translation import gettext_lazy as _

class PaymentMethod(models.Model):
    class Provider(models.TextChoices):
        MANUAL = 'MANUAL', _('Manual (Send Money)')
        SSLCOMMERZ = 'SSLCOMMERZ', _('SSLCommerz')
        BKASH_API = 'BKASH_API', _('Bkash API')
        NAGAD_API = 'NAGAD_API', _('Nagad API')
        COD = 'COD', _('Cash on Delivery')

    name = models.CharField(max_length=50) # e.g. "Bkash Personal", "Nagad"
    provider = models.CharField(max_length=20, choices=Provider.choices, default=Provider.MANUAL)
    account_number = models.CharField(max_length=20, blank=True, help_text="For manual payment")
    instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='payments/methods/', blank=True, null=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        VERIFIED = 'VERIFIED', _('Verified')
        FAILED = 'FAILED', _('Failed')
        REFUNDED = 'REFUNDED', _('Refunded')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions', db_index=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True, db_index=True)
    method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True, help_text="TrxID from SMS or Gateway", db_index=True)
    sender_number = models.CharField(max_length=20, blank=True, help_text="Number from which money was sent", db_index=True)
    reference = models.CharField(max_length=100, blank=True, help_text="Reference used during transfer")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)

    # Webhook Data
    raw_data = models.TextField(blank=True, help_text="Raw SMS or Gateway response")

    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_transactions')
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"

class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'PERCENTAGE', _('Percentage')
        FIXED_AMOUNT = 'FIXED_AMOUNT', _('Fixed Amount')

    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices, default=DiscountType.FIXED_AMOUNT)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    is_active = models.BooleanField(default=True, db_index=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    usage_limit = models.PositiveIntegerField(default=0, help_text="0 for unlimited")
    used_count = models.PositiveIntegerField(default=0)

    is_free_shipping = models.BooleanField(default=False)

    def __str__(self):
        return self.code

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet of {self.user} ({self.balance})"

class WalletTransaction(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = 'DEPOSIT', _('Deposit')
        WITHDRAWAL = 'WITHDRAWAL', _('Withdrawal')
        REFUND = 'REFUND', _('Refund')
        PURCHASE = 'PURCHASE', _('Purchase')

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions', db_index=True)
    transaction_type = models.CharField(max_length=20, choices=Type.choices, db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    reference_id = models.CharField(max_length=100, blank=True, help_text="Related Order ID or TrxID")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
