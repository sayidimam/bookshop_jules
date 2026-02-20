from django.contrib import admin
from .models import AffiliateProgram, AffiliateLink, AffiliateClick, AffiliateCommission

@admin.register(AffiliateProgram)
class AffiliateProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'commission_percentage', 'is_active')

@admin.register(AffiliateLink)
class AffiliateLinkAdmin(admin.ModelAdmin):
    list_display = ('unique_code', 'user', 'program', 'clicks', 'created_at')
    search_fields = ('unique_code', 'user__phone_number')
    readonly_fields = ('clicks', 'created_at')

@admin.register(AffiliateCommission)
class AffiliateCommissionAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'link', 'amount', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
