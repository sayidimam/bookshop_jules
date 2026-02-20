from django.contrib import admin
from .models import Supplier, PurchaseOrder, PurchaseItem, StockLog

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'contact_person', 'is_active')
    search_fields = ('name', 'phone')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'supplier', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'supplier')
    search_fields = ('reference_number', 'supplier__name')
    inlines = [PurchaseItemInline]

@admin.register(StockLog)
class StockLogAdmin(admin.ModelAdmin):
    list_display = ('book', 'action', 'quantity', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('book__title', 'reference')
    readonly_fields = ('created_at',)
