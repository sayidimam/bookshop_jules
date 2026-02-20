from django.db import models
from django.conf import settings
from decimal import Decimal
from django.utils import timezone
import uuid

class GiftCard(models.Model):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sent_gift_cards')
    recipient_email = models.EmailField(blank=True)
    recipient_phone = models.CharField(max_length=20, blank=True)

    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"GIFT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} ({self.current_balance})"

class GiftCardUsage(models.Model):
    gift_card = models.ForeignKey(GiftCard, on_delete=models.CASCADE, related_name='usages')
    order_id = models.IntegerField(help_text="ID of the order where used")
    amount_used = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gift_card.code} used {self.amount_used}"
