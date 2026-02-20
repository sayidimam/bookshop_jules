from django.urls import path
from .views import SmsWebhookView

urlpatterns = [
    path('sms-webhook/', SmsWebhookView.as_view(), name='sms-webhook'),
    # Add other integration endpoints here as needed (e.g. SSLCommerz callbacks)
]
