from django.urls import path
from .views import PaymentVerifyView, PaymentMethodListView
from .webhook import SmsWebhookView

urlpatterns = [
    path('verify/', PaymentVerifyView.as_view(), name='payment-verify'),
    path('methods/', PaymentMethodListView.as_view(), name='payment-methods'),
    path('webhook/sms/', SmsWebhookView.as_view(), name='sms-webhook'),
]
