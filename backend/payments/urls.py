from django.urls import path
from .views import PaymentVerifyView, PaymentMethodListView

urlpatterns = [
    path('verify/', PaymentVerifyView.as_view(), name='payment-verify'),
    path('methods/', PaymentMethodListView.as_view(), name='payment-methods'),
]
