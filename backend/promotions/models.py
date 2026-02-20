from django.db import models
from django.utils.translation import gettext_lazy as _
from catalog.models import Book, Category

class Offer(models.Model):
    class Type(models.TextChoices):
        BOGO = 'BOGO', _('Buy One Get One')
        BUNDLE = 'BUNDLE', _('Bundle Discount')
        TIERED = 'TIERED', _('Tiered Discount')
        FLAT = 'FLAT', _('Flat Discount')

    name = models.CharField(max_length=255, db_index=True)
    offer_type = models.CharField(max_length=20, choices=Type.choices)

    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)

    is_active = models.BooleanField(default=True, db_index=True)
    priority = models.IntegerField(default=0, help_text="Higher priority applies first")

    description = models.TextField(blank=True)
    banner = models.ImageField(upload_to='offers/', blank=True, null=True)

    def __str__(self):
        return self.name

class OfferCondition(models.Model):
    class Logic(models.TextChoices):
        MIN_QTY = 'MIN_QTY', _('Minimum Quantity')
        MIN_AMOUNT = 'MIN_AMOUNT', _('Minimum Amount')
        SPECIFIC_BOOK = 'SPECIFIC_BOOK', _('Specific Book')
        SPECIFIC_CATEGORY = 'SPECIFIC_CATEGORY', _('Specific Category')

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='conditions')
    logic = models.CharField(max_length=20, choices=Logic.choices)

    # Generic target (could be book ID, Category ID, or Amount)
    target_id = models.IntegerField(null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Qty or Amount")

    def __str__(self):
        return f"{self.logic} >= {self.value}"

class OfferReward(models.Model):
    class Type(models.TextChoices):
        DISCOUNT_PERCENT = 'DISCOUNT_PERCENT', _('Percentage Discount')
        DISCOUNT_AMOUNT = 'DISCOUNT_AMOUNT', _('Fixed Amount Discount')
        FREE_ITEM = 'FREE_ITEM', _('Free Item')
        FREE_SHIPPING = 'FREE_SHIPPING', _('Free Shipping')

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='rewards')
    reward_type = models.CharField(max_length=20, choices=Type.choices)
    value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Percent or Amount")

    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.reward_type}: {self.value}"
