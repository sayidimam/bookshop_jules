from django.contrib import admin
from .models import Division, District, Thana, ShippingZone, ShippingRate, OverweightCharge, Courier
from .models_collector import CollectorTask, TaskItem
from .models_audit import CourierAccount, CourierConsignment, CourierLedger, CourierDispute

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'bn_name')
    search_fields = ('name', 'bn_name')

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'division', 'bn_name')
    search_fields = ('name', 'bn_name')
    list_filter = ('division',)

@admin.register(Thana)
class ThanaAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'bn_name', 'zone')
    search_fields = ('name', 'bn_name')
    list_filter = ('district', 'zone')

@admin.register(ShippingZone)
class ShippingZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')

@admin.register(ShippingRate)
class ShippingRateAdmin(admin.ModelAdmin):
    list_display = ('zone', 'max_weight', 'rate')
    list_filter = ('zone',)

@admin.register(OverweightCharge)
class OverweightChargeAdmin(admin.ModelAdmin):
    list_display = ('zone', 'apply_above_weight', 'charge_per_unit', 'unit_weight')
    list_filter = ('zone',)

@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')

class TaskItemInline(admin.TabularInline):
    model = TaskItem
    extra = 1

@admin.register(CollectorTask)
class CollectorTaskAdmin(admin.ModelAdmin):
    list_display = ('collector', 'status', 'supplier', 'created_at')
    list_filter = ('status', 'collector', 'created_at')
    search_fields = ('collector__phone_number', 'note')
    inlines = [TaskItemInline]

@admin.register(CourierAccount)
class CourierAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'is_active')
    list_filter = ('provider', 'is_active')

@admin.register(CourierConsignment)
class CourierConsignmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'account', 'status', 'expected_cod', 'is_paid_by_courier')
    list_filter = ('is_paid_by_courier', 'account', 'status')
    search_fields = ('tracking_code', 'consignment_id')

@admin.register(CourierLedger)
class CourierLedgerAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'transaction_ref', 'date_received')
    list_filter = ('account', 'date_received')

@admin.register(CourierDispute)
class CourierDisputeAdmin(admin.ModelAdmin):
    list_display = ('consignment', 'reason', 'claimed_amount', 'status')
    list_filter = ('status', 'reason')
