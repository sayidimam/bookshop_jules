from rest_framework import serializers
from .models import Transaction, PaymentMethod

class PaymentVerifySerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    transaction_id = serializers.CharField(max_length=100)
    payment_method_id = serializers.IntegerField(required=False)

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'provider', 'account_number', 'instructions', 'logo']
