from django.db import models
from django.conf import settings
from orders.models import Order, OrderItem
from django.utils.translation import gettext_lazy as _

class ReturnRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')
        COMPLETED = 'COMPLETED', _('Completed')

    class Reason(models.TextChoices):
        DAMAGED = 'DAMAGED', _('Damaged Product')
        WRONG_ITEM = 'WRONG_ITEM', _('Wrong Item Sent')
        MIND_CHANGED = 'MIND_CHANGED', _('Mind Changed')
        OTHER = 'OTHER', _('Other')

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='return_requests', db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    reason = models.CharField(max_length=50, choices=Reason.choices)
    description = models.TextField(blank=True)

    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return #{self.id} for Order #{self.order.id}"

class ReturnItem(models.Model):
    return_request = models.ForeignKey(ReturnRequest, on_delete=models.CASCADE, related_name='items')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    condition = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.order_item.book.title}"
