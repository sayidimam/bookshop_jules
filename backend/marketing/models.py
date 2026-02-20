from django.db import models
from django.conf import settings
from catalog.models import Book

class AffiliateProgram(models.Model):
    name = models.CharField(max_length=255)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class AffiliateLink(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='affiliate_links')
    program = models.ForeignKey(AffiliateProgram, on_delete=models.SET_NULL, null=True)

    unique_code = models.CharField(max_length=20, unique=True, db_index=True)
    target_url = models.URLField(help_text="Where the link redirects")

    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.unique_code}"

class AffiliateClick(models.Model):
    link = models.ForeignKey(AffiliateLink, on_delete=models.CASCADE, related_name='click_logs')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Click on {self.link.unique_code}"

class AffiliateCommission(models.Model):
    link = models.ForeignKey(AffiliateLink, on_delete=models.CASCADE)
    order_id = models.IntegerField(db_index=True) # Soft link to Order
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission {self.amount} for Order {self.order_id}"
