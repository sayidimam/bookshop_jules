from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('phone_number', 'email', 'full_name', 'role', 'is_staff', 'is_active')
    search_fields = ('phone_number', 'email', 'full_name')
    ordering = ('phone_number',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Role & Tracking', {'fields': ('role', 'fbp', 'fbc', 'ip_address', 'user_agent')}),
    )

admin.site.register(User, UserAdmin)
