from django.db import models
from django.utils.translation import gettext_lazy as _
from catalog.models import Book

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    contact_person = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        ORDERED = 'ORDERED', _('Ordered')
        RECEIVED = 'RECEIVED', _('Received')
        CANCELLED = 'CANCELLED', _('Cancelled')

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_orders')
    reference_number = models.CharField(max_length=50, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    note = models.TextField(blank=True)

    expected_date = models.DateField(null=True, blank=True)
    received_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PO-{self.id} ({self.supplier.name})"

class PurchaseItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cost price per unit")

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

class StockLog(models.Model):
    class Action(models.TextChoices):
        PURCHASE = 'PURCHASE', _('Purchase Received')
        SALE = 'SALE', _('Sale')
        RETURN_IN = 'RETURN_IN', _('Return In')
        RETURN_OUT = 'RETURN_OUT', _('Return Out (To Supplier)')
        ADJUSTMENT = 'ADJUSTMENT', _('Inventory Adjustment')
        DAMAGE = 'DAMAGE', _('Damage/Waste')
        INTERNAL_USE = 'INTERNAL_USE', _('Internal Consumption')

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='stock_logs', db_index=True)
    action = models.CharField(max_length=20, choices=Action.choices)
    quantity = models.IntegerField(help_text="Positive for add, negative for remove")

    reference = models.CharField(max_length=100, blank=True, help_text="Order ID or PO Number")
    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.book.title} - {self.action} ({self.quantity})"

# Import split models
from .models_warehouse import *
from .models_internal import *
