from django.contrib import admin
from .models import UserActivity, SearchTerm

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'book', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__phone_number', 'ip_address')
    readonly_fields = ('created_at',)

@admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    list_display = ('term', 'count', 'last_searched')
    search_fields = ('term',)
    ordering = ('-count',)
