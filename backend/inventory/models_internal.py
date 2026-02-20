from django.db import models
from django.conf import settings
from catalog.models import Book
from .models_warehouse import Warehouse

class DamageLog(models.Model):
    class Reason(models.TextChoices):
        PRINTING_ERROR = 'PRINTING_ERROR', 'Printing Error'
        WATER_DAMAGE = 'WATER_DAMAGE', 'Water Damage'
        TORN_PAGES = 'TORN_PAGES', 'Torn Pages'
        LOST_IN_TRANSIT = 'LOST_IN_TRANSIT', 'Lost in Transit'
        OTHER = 'OTHER', 'Other'

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='damages')
    quantity = models.PositiveIntegerField(default=1)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)

    reason = models.CharField(max_length=50, choices=Reason.choices)
    description = models.TextField(blank=True)

    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} (Damaged)"

class InternalConsumption(models.Model):
    class Purpose(models.TextChoices):
        GIFT = 'GIFT', 'Gift to Guest'
        OFFICE_USE = 'OFFICE_USE', 'Office Use'
        REVIEW_COPY = 'REVIEW_COPY', 'Review Copy'
        EMPLOYEE_PERK = 'EMPLOYEE_PERK', 'Employee Perk'
        OTHER = 'OTHER', 'Other'

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='internal_consumptions')
    quantity = models.PositiveIntegerField(default=1)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)

    taken_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='consumed_items')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='approved_consumptions')

    purpose = models.CharField(max_length=50, choices=Purpose.choices)
    note = models.TextField(blank=True)

    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} ({self.purpose})"
