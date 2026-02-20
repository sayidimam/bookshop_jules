from rest_framework import serializers
from .models import Order, OrderItem, OrderStatusHistory
from catalog.models import Book
from logistics.models import Thana, District, Division, ShippingZone, ShippingRate, OverweightCharge
from users.serializers import UserSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_cover = serializers.ImageField(source='book.cover_image', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'book_title', 'book_cover', 'quantity', 'price', 'status']

class OrderHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.StringRelatedField()
    class Meta:
        model = OrderStatusHistory
        fields = ['old_status', 'new_status', 'changed_by', 'timestamp', 'note']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    history = OrderHistorySerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class CartItemSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)

class CheckoutSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)

    # Shipping Info
    shipping_name = serializers.CharField(max_length=255)
    shipping_phone = serializers.CharField(max_length=20)
    shipping_address = serializers.CharField()
    shipping_thana_id = serializers.IntegerField()

    payment_method = serializers.CharField(required=False, default='COD')
    note = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        # Validate Thana
        try:
            thana = Thana.objects.get(pk=attrs['shipping_thana_id'])
            attrs['thana_obj'] = thana
        except Thana.DoesNotExist:
            raise serializers.ValidationError({'shipping_thana_id': 'Invalid Thana ID'})

        # Validate Stock
        for item in attrs['items']:
            try:
                book = Book.objects.get(pk=item['book_id'])
                if book.stock < item['quantity']:
                    # raise serializers.ValidationError(f"Insufficient stock for {book.title}")
                    pass # Allow ordering for now (Preorder logic possible)
                item['book_obj'] = book
            except Book.DoesNotExist:
                raise serializers.ValidationError(f"Book ID {item['book_id']} not found")

        return attrs
