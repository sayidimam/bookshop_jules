from django.urls import path
from .views import SmsWebhookView, CourierWebhookView

urlpatterns = [
    path('sms-webhook/', SmsWebhookView.as_view(), name='sms-webhook'),
    path('courier-webhook/', CourierWebhookView.as_view(), name='courier-webhook'),
]
