from django.db import models
from django.utils.translation import gettext_lazy as _
from catalog.models import Book

class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    manager_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class StockItem(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='warehouse_stock')
    quantity = models.PositiveIntegerField(default=0)
    rack_location = models.CharField(max_length=50, blank=True, help_text="e.g. A-12-3")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('warehouse', 'book')

    def __str__(self):
        return f"{self.book.title} in {self.warehouse.name} ({self.quantity})"
