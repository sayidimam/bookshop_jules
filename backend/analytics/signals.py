from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Order)
def track_order_events(sender, instance, created, **kwargs):
    if instance.status == Order.Status.CONFIRMED:
        # Mocking Server-Side Tracking (Facebook CAPI / Google Measurement Protocol)
        track_purchase_event(instance)

def track_purchase_event(order):
    user_data = {
        'phone': order.shipping_phone,
        'fbp': order.user.fbp if order.user else None,
        'fbc': order.user.fbc if order.user else None,
        'ip': order.user.ip_address if order.user else None,
        'agent': order.user.user_agent if order.user else None,
    }

    event_data = {
        'event_name': 'Purchase',
        'event_time': int(order.updated_at.timestamp()),
        'user_data': user_data,
        'custom_data': {
            'currency': 'BDT',
            'value': float(order.total_amount),
            'order_id': order.id,
            'content_ids': [item.book.id for item in order.items.all()],
            'content_type': 'product'
        }
    }

    logger.info(f"TRACKING: Purchase Event Sent for Order #{order.id}: {event_data}")
    # In production: requests.post('https://graph.facebook.com/v19.0/PIXEL_ID/events', json=payload)
