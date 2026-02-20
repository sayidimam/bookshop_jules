from django.db import models
from django.conf import settings
from orders.models import Order
from orders.models_return import ReturnRequest
from .models import Wallet, WalletTransaction

class Refund(models.Model):
    class Method(models.TextChoices):
        WALLET = 'WALLET', 'Wallet Balance'
        BKASH = 'BKASH', 'Bkash'
        NAGAD = 'NAGAD', 'Nagad'
        BANK = 'BANK', 'Bank Transfer'
        CASH = 'CASH', 'Cash'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        COMPLETED = 'COMPLETED', 'Completed'
        REJECTED = 'REJECTED', 'Rejected'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refunds')
    return_request = models.ForeignKey(ReturnRequest, on_delete=models.SET_NULL, null=True, blank=True, related_name='refunds')

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=Method.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    # Banking/Mobile Banking Info
    account_number = models.CharField(max_length=50, blank=True, help_text="Customer's account number")
    transaction_ref = models.CharField(max_length=100, blank=True, help_text="TrxID of the refund sent")

    admin_note = models.TextField(blank=True)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Refund {self.amount} for Order #{self.order.id}"

    def save(self, *args, **kwargs):
        # Auto-process Wallet Refunds
        if self.status == self.Status.COMPLETED and self.method == self.Method.WALLET:
            if not WalletTransaction.objects.filter(reference_id=f"REFUND-{self.id}").exists():
                wallet, _ = Wallet.objects.get_or_create(user=self.order.user)
                wallet.balance += self.amount
                wallet.save()

                WalletTransaction.objects.create(
                    wallet=wallet,
                    transaction_type=WalletTransaction.Type.REFUND,
                    amount=self.amount,
                    description=f"Refund for Order #{self.order.id}",
                    reference_id=f"REFUND-{self.id}"
                )
        super().save(*args, **kwargs)
