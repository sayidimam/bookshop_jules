from django.db import models
from django.conf import settings
from catalog.models import Book
from orders.models import Order
from inventory.models import Supplier

class CollectorTask(models.Model):
    class Status(models.TextChoices):
        ASSIGNED = 'ASSIGNED', 'Assigned'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        PARTIAL_COLLECTED = 'PARTIAL_COLLECTED', 'Partial Collected'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    collector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks', db_index=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_collector_tasks')

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ASSIGNED, db_index=True)

    # Optional: Link to a specific Supplier (Market/Shop)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task #{self.id} for {self.collector}"

class TaskItem(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COLLECTED = 'COLLECTED', 'Collected'
        NOT_FOUND = 'NOT_FOUND', 'Not Found (Unavailable)'

    task = models.ForeignKey(CollectorTask, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # Link back to the customer order requiring this book
    order_ref = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    collected_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} ({self.status})"
