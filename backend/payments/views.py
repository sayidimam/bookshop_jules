from rest_framework import views, status, generics, permissions
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .models import MobilePaymentLog, Transaction, PaymentMethod
from .serializers import PaymentVerifySerializer, PaymentMethodSerializer
from orders.models import Order

class PaymentVerifyView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PaymentVerifySerializer(data=request.data)
        if serializer.is_valid():
            trx_id = serializer.validated_data['transaction_id']
            order_id = serializer.validated_data['order_id']

            try:
                order = Order.objects.get(id=order_id, user=request.user)
            except Order.DoesNotExist:
                return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

            # Check MobilePaymentLog
            # Logic: Match exactly TrxID and ensure not claimed.
            # Also handle Reference matching if user provided reference during payment

            try:
                # Primary Check: Transaction ID
                log = MobilePaymentLog.objects.get(transaction_id=trx_id, is_claimed=False)

                with transaction.atomic():
                    # Claim Log
                    log.is_claimed = True
                    log.claimed_at = timezone.now()
                    log.save()

                    # Create Transaction
                    trx = Transaction.objects.create(
                        user=request.user,
                        order=order,
                        amount=log.amount,
                        transaction_id=trx_id,
                        sender_number=log.sender_number,
                        reference=log.reference,
                        status=Transaction.Status.VERIFIED,
                        mobile_log=log,
                        verified_at=timezone.now()
                    )

                    # Update Order
                    order.paid_amount += log.amount
                    if order.paid_amount >= order.total_amount:
                        order.status = Order.Status.CONFIRMED
                    else:
                        order.status = Order.Status.PROCESSING # Partial payment

                    order.save()

                return Response({'message': 'Payment Verified', 'amount': log.amount}, status=status.HTTP_200_OK)

            except MobilePaymentLog.DoesNotExist:
                return Response({'error': 'Invalid Transaction ID or already used.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentMethodListView(generics.ListAPIView):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.AllowAny]
