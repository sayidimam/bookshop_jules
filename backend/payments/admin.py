from django.contrib import admin
from .models import PaymentMethod, Transaction, Coupon

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'is_active')
    list_filter = ('is_active',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order', 'status', 'amount', 'created_at')
    list_filter = ('status', 'method', 'created_at')
    search_fields = ('transaction_id', 'sender_number', 'reference', 'order__id')
    readonly_fields = ('created_at', 'verified_at', 'verified_by')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'is_active', 'valid_to', 'used_count')
    list_filter = ('is_active', 'discount_type')
    search_fields = ('code', 'description')
