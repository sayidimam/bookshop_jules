from django.contrib import admin
from .models import PaymentMethod, Transaction, Coupon, Wallet, WalletTransaction

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

class WalletTransactionInline(admin.TabularInline):
    model = WalletTransaction
    extra = 0
    can_delete = False
    readonly_fields = ('transaction_type', 'amount', 'description', 'reference_id', 'created_at')

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'updated_at')
    search_fields = ('user__phone_number', 'user__full_name')
    inlines = [WalletTransactionInline]
