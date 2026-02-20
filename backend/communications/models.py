from django.db import models
from django.conf import settings

class NotificationLog(models.Model):
    class Type(models.TextChoices):
        SMS = 'SMS', 'SMS'
        EMAIL = 'EMAIL', 'Email'
        PUSH = 'PUSH', 'Push Notification'

    class Status(models.TextChoices):
        SENT = 'SENT', 'Sent'
        FAILED = 'FAILED', 'Failed'
        QUEUED = 'QUEUED', 'Queued'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', db_index=True)
    notification_type = models.CharField(max_length=20, choices=Type.choices)

    recipient = models.CharField(max_length=255, help_text="Phone number or Email")
    content = models.TextField()

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED, db_index=True)
    error_message = models.TextField(blank=True)

    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.notification_type} to {self.recipient} ({self.status})"

class MessageTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g. ORDER_CONFIRMED")
    title = models.CharField(max_length=255, blank=True, help_text="Email Subject or Push Title")
    body = models.TextField(help_text="Use placeholders like {{ name }}, {{ order_id }}")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
