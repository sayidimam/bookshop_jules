from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models_return import ReturnRequest
from inventory.models_warehouse import StockItem
from inventory.models_internal import DamageLog
from inventory.models import StockLog

@receiver(pre_save, sender=ReturnRequest)
def track_previous_status(sender, instance, **kwargs):
    """
    Track the previous status before saving to detect changes.
    """
    if instance.id:
        try:
            previous_instance = ReturnRequest.objects.get(id=instance.id)
            instance._previous_status = previous_instance.status
        except ReturnRequest.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None

@receiver(post_save, sender=ReturnRequest)
def handle_return_restocking(sender, instance, created, **kwargs):
    """
    Automated logic to handle stock updates when a ReturnRequest transitions to COMPLETED.
    """
    # Check if status CHANGED to COMPLETED
    previous_status = getattr(instance, '_previous_status', None)

    if instance.status == 'COMPLETED' and previous_status != 'COMPLETED':
        for item in instance.items.all():
            book = item.order_item.book
            qty = item.quantity

            # Logic A: If Good Condition -> Return to Stock
            if item.condition == 'GOOD':
                # Try to return to the specific warehouse if tracked, otherwise first available
                # In a real scenario, ReturnRequest should likely have a 'warehouse' field.
                # For now, defaulting to the first active warehouse containing this book or any warehouse.
                stock_item = StockItem.objects.filter(book=book).first()

                if stock_item:
                    stock_item.quantity += qty
                    stock_item.save()

                    # Log the movement
                    StockLog.objects.create(
                        book=book,
                        action=StockLog.Action.RETURN_IN,
                        quantity=qty,
                        reference=f"Return #{instance.id}",
                        note=f"Restocked to {stock_item.warehouse.name}"
                    )

            # Logic B: If Damaged -> Log Damage
            elif item.condition == 'DAMAGED':
                DamageLog.objects.create(
                    book=book,
                    quantity=qty,
                    reason=DamageLog.Reason.OTHER, # Or map from return reason
                    description=f"Return #{instance.id} - {instance.reason}",
                    reported_by=instance.user
                )
