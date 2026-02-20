from django.contrib import admin
from .models import NotificationLog, MessageTemplate

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'status', 'sent_at', 'created_at')
    list_filter = ('notification_type', 'status', 'created_at')
    search_fields = ('recipient', 'content')
    readonly_fields = ('created_at', 'sent_at')

@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'is_active')
    search_fields = ('name', 'body')
