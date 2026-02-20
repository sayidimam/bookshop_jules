from django.contrib import admin
from .models import Offer, OfferCondition, OfferReward

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
