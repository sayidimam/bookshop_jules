from django.db import models
from django.conf import settings
from catalog.models import Book
from logistics.models import Courier, Division, District, Thana
from django.utils.translation import gettext_lazy as _

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

class Order(models.Model):
    class Status(models.TextChoices):
        # Lead Generation Stage
        INCOMPLETE = 'INCOMPLETE', _('Incomplete (Lead)')  # Phone captured, checkout not finished

        # Order Placement Stages
        QUEUE = 'QUEUE', _('Queue')  # High traffic buffer
        PROCESSING = 'PROCESSING', _('Processing')  # Placed, Payment Pending/COD

        # Pre-fulfillment Stages
        NO_RESPONSE = 'NO_RESPONSE', _('Good But No Response')
        ON_HOLD = 'ON_HOLD', _('On Hold')
        CONFIRMED = 'CONFIRMED', _('Confirmed')  # Payment Verified
        CANCELLED = 'CANCELLED', _('Cancelled')

        # Fulfillment Stages (After Confirmation)
        PENDING = 'PENDING', _('Pending')  # Ready for fulfillment
        COLLECTING = 'COLLECTING', _('Collecting')
        HOLD_COLLECTING = 'HOLD_COLLECTING', _('Hold (Collecting)')
        PACKING = 'PACKING', _('Packing')
        RTS = 'RTS', _('Ready to Ship (RTS)')
        SHIPPED = 'SHIPPED', _('Shipped')
        DELIVERED = 'DELIVERED', _('Delivered')

        # Returns & Issues
        RETURN_REQUEST = 'RETURN_REQUEST', _('Return Request')
        PENDING_RETURN = 'PENDING_RETURN', _('Pending Return')
        RETURNED = 'RETURNED', _('Returned')
        PARTIAL = 'PARTIAL', _('Partial Delivery')
        PENDING_CANCEL = 'PENDING_CANCEL', _('Pending Cancel')
        PREORDER = 'PREORDER', _('Preorder')
        LOST = 'LOST', _('Lost')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='orders', db_index=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.INCOMPLETE, db_index=True)

    # Lead Management
    is_lead = models.BooleanField(default=False, db_index=True, help_text="True if order is incomplete but phone is captured")
    lead_score = models.IntegerField(default=0, help_text="Priority score for sales team")

    # Address Details (Snapshot)
    # Allow blank for incomplete leads
    shipping_name = models.CharField(max_length=255, blank=True)
    shipping_phone = models.CharField(max_length=20, db_index=True)
    shipping_address = models.TextField(blank=True)
    shipping_division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_thana = models.ForeignKey(Thana, on_delete=models.SET_NULL, null=True, blank=True)

    # Financials
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # Logistics
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    tracking_id = models.CharField(max_length=100, blank=True, db_index=True)
    weight = models.DecimalField(max_digits=8, decimal_places=3, default=0.00, help_text="Total Weight in KG")

    # Payment Info
    payment_method = models.CharField(max_length=50, blank=True) # e.g. COD, BKASH, NAGAD
    transaction_id = models.CharField(max_length=100, blank=True, db_index=True)

    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

class OrderItem(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        COLLECTED = 'COLLECTED', _('Collected')
        OUT_OF_STOCK = 'OUT_OF_STOCK', _('Out of Stock')
        PACKED = 'PACKED', _('Packed')

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.PROTECT) # Don't delete order history if book is deleted? Better PROTECT.
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Unit price at time of order")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} (Order #{self.order.id})"

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='history', db_index=True)
    old_status = models.CharField(max_length=30, blank=True)
    new_status = models.CharField(max_length=30)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Order #{self.order.id}: {self.old_status} -> {self.new_status}"

# Import split models
from .models_advanced import *
from .models_archive import *
from .models_return import *
