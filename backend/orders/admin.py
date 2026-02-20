from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, OrderStatusHistory
from .models_return import ReturnRequest, ReturnItem
from .models_advanced import PreOrder, SubscriptionPlan, UserSubscription

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ('book',)

class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('old_status', 'new_status', 'changed_by', 'timestamp', 'note')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at', 'courier')
    list_filter = ('status', 'courier', 'created_at', 'payment_method')
    search_fields = ('id', 'user__phone_number', 'tracking_id', 'transaction_id')
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'status', 'created_at', 'updated_at', 'note')
        }),
        ('Shipping Details', {
            'fields': ('shipping_name', 'shipping_phone', 'shipping_address', 'shipping_division', 'shipping_district', 'shipping_thana', 'courier', 'tracking_id', 'weight')
        }),
        ('Financials', {
            'fields': ('total_amount', 'shipping_charge', 'discount_amount', 'paid_amount', 'payment_method', 'transaction_id')
        }),
    )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'book', 'quantity')

class ReturnItemInline(admin.TabularInline):
    model = ReturnItem
    extra = 0

@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'status', 'reason', 'created_at')
    list_filter = ('status', 'reason', 'created_at')
    search_fields = ('order__id', 'user__phone_number')
    inlines = [ReturnItemInline]

@admin.register(PreOrder)
class PreOrderAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'status', 'advance_payment', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('book__title', 'user__phone_number')

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'is_active')

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'end_date', 'is_active')
