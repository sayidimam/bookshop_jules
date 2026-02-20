from rest_framework import views, status, generics, permissions, filters
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from decimal import Decimal, ROUND_UP
from .models import Order, OrderItem, OrderStatusHistory
from .serializers import CheckoutSerializer, OrderSerializer
from logistics.models import ShippingRate, OverweightCharge
from integrations.greenweb import GreenwebClient
from analytics.models import SiteConfiguration
from analytics.signals import track_purchase_event

class CheckoutView(views.APIView):
    permission_classes = [permissions.AllowAny] # Allow guest checkout (will link if user exists via phone)

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            thana = data['thana_obj']
            items = data['items']

            # 1. Calculate Total Weight and Price
            total_weight = Decimal(0)
            total_price = Decimal(0)

            for item in items:
                book = item['book_obj']
                qty = item['quantity']
                weight = book.weight or Decimal(0.25)
                total_weight += weight * qty

                price = book.sale_price if book.sale_price else book.regular_price
                total_price += price * qty

            # 2. Calculate Shipping
            shipping_charge = Decimal(60) # Fallback default
            if thana.zone:
                rates = thana.zone.rates.all().order_by('max_weight')
                rate_found = False
                for rate in rates:
                    if total_weight <= rate.max_weight:
                        shipping_charge = rate.rate
                        rate_found = True
                        break

                if not rate_found and rates.exists():
                    # Overweight Logic
                    max_rate = rates.last()
                    shipping_charge = max_rate.rate

                    overcharges = thana.zone.overweight_charges.all()
                    for oc in overcharges:
                        if total_weight > oc.apply_above_weight:
                            extra_weight = total_weight - oc.apply_above_weight
                            # Ceiling division logic for units
                            units = (extra_weight / oc.unit_weight).quantize(Decimal("1."), rounding='ROUND_UP')
                            shipping_charge += units * oc.charge_per_unit
                            break

            # 3. Create Order
            with transaction.atomic():
                user = request.user if request.user.is_authenticated else None
                # TODO: Link guest user by phone if exists logic

                order = Order.objects.create(
                    user=user,
                    shipping_name=data['shipping_name'],
                    shipping_phone=data['shipping_phone'],
                    shipping_address=data['shipping_address'],
                    shipping_thana=thana,
                    shipping_district=thana.district,
                    shipping_division=thana.district.division,
                    total_amount=total_price + shipping_charge, # Will be updated
                    shipping_charge=shipping_charge,
                    weight=total_weight,
                    payment_method=data.get('payment_method', 'COD'),
                    note=data.get('note', ''),
                    status=Order.Status.INCOMPLETE # Or QUEUE
                )

                for item in items:
                    book = item['book_obj']
                    price = book.sale_price if book.sale_price else book.regular_price
                    OrderItem.objects.create(
                        order=order,
                        book=book,
                        quantity=item['quantity'],
                        price=price
                    )

                # Finalize
                order.status = Order.Status.QUEUE
                order.save()

                OrderStatusHistory.objects.create(
                    order=order,
                    new_status=Order.Status.QUEUE,
                    note="Order Placed via Checkout"
                )

                # 4. SMS Notification
                try:
                    sms_client = GreenwebClient()
                    msg = f"আপনার অর্ডার #{order.id} প্লেস করা হয়েছে। কনফার্মেশনের জন্য অপেক্ষা করুন।"
                    sms_client.send_sms(order.shipping_phone, msg)
                except Exception as e:
                    print(f"Failed to send SMS: {e}")

                # 5. Tracking Event (If Configured for Checkout)
                try:
                    config = SiteConfiguration.objects.first()
                    if not config or config.tracking_trigger == SiteConfiguration.TrackingTrigger.ON_CHECKOUT:
                        track_purchase_event(order)
                except Exception as e:
                    print(f"Tracking Error: {e}")

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'shipping_phone', 'transaction_id']
    ordering_fields = ['created_at', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            status_param = self.request.query_params.get('status')
            qs = Order.objects.all()
            if status_param:
                qs = qs.filter(status=status_param)
            return qs
        return Order.objects.filter(user=user)

class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        old_status = self.get_object().status
        instance = serializer.save()
        new_status = instance.status

        if old_status != new_status:
            OrderStatusHistory.objects.create(
                order=instance,
                old_status=old_status,
                new_status=new_status,
                changed_by=self.request.user
            )
            # Signal could be triggered here for tracking
