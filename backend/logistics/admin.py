from django.contrib import admin
from .models import Division, District, Thana, ShippingZone, ShippingRate, OverweightCharge, Courier
from .models_collector import CollectorTask, TaskItem

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
