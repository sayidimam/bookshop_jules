from django.db import models
from django.conf import settings
from catalog.models import Book
from django.utils.translation import gettext_lazy as _

class PreOrder(models.Model):
    class Status(models.TextChoices):
        INTERESTED = 'INTERESTED', _('Interested')
        BOOKED = 'BOOKED', _('Booked (Paid)')
        NOTIFIED = 'NOTIFIED', _('Notified')
        CONVERTED = 'CONVERTED', _('Converted to Order')
        CANCELLED = 'CANCELLED', _('Cancelled')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preorders')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='preorders')

    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INTERESTED)

    advance_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preorder {self.book.title} by {self.user.phone_number}"

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(help_text="Duration in days")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.phone_number} - {self.plan.name}"
