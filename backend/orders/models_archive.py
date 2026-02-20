from django.db import models

class OrderArchive(models.Model):
    """
    Flat structure for archiving old orders (2+ years).
    No ForeignKeys to maintain independence if referenced users/books are deleted.
    """
    original_order_id = models.BigIntegerField(db_index=True)
    user_data = models.JSONField(help_text="Snapshot of user info")
    items_data = models.JSONField(help_text="List of items, prices, qty")

    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    order_date = models.DateTimeField(db_index=True)
    archived_at = models.DateTimeField(auto_now_add=True)

    status_history = models.TextField(blank=True)

    def __str__(self):
        return f"Archive of #{self.original_order_id}"
