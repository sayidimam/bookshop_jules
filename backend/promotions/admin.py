from django.contrib import admin
from .models import Offer, OfferCondition, OfferReward
from .models_giftcard import GiftCard, GiftCardUsage

class OfferConditionInline(admin.TabularInline):
    model = OfferCondition
    extra = 1

class OfferRewardInline(admin.TabularInline):
    model = OfferReward
    extra = 1

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'offer_type', 'start_date', 'end_date', 'is_active', 'priority')
    list_filter = ('offer_type', 'is_active')
    search_fields = ('name',)
    inlines = [OfferConditionInline, OfferRewardInline]

class GiftCardUsageInline(admin.TabularInline):
    model = GiftCardUsage
    extra = 0
    readonly_fields = ('used_at', 'amount_used', 'order_id')

@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = ('code', 'current_balance', 'expiry_date', 'is_active')
    search_fields = ('code', 'recipient_email')
    inlines = [GiftCardUsageInline]
