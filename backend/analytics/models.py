from django.db import models
from django.conf import settings
from catalog.models import Book

class UserActivity(models.Model):
    class Type(models.TextChoices):
        VIEW_PRODUCT = 'VIEW_PRODUCT', 'View Product'
        ADD_TO_CART = 'ADD_TO_CART', 'Add to Cart'
        SEARCH = 'SEARCH', 'Search'
        FILTER = 'FILTER', 'Filter'
        LOGIN = 'LOGIN', 'Login'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    session_key = models.CharField(max_length=40, blank=True, db_index=True)

    activity_type = models.CharField(max_length=20, choices=Type.choices, db_index=True)

    # Context
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.activity_type} by {self.user or 'Guest'}"

class SearchTerm(models.Model):
    term = models.CharField(max_length=255, db_index=True)
    count = models.PositiveIntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.term} ({self.count})"
