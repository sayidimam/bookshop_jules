from django.db import models
from django.utils.translation import gettext_lazy as _

class SiteConfiguration(models.Model):
    class TrackingTrigger(models.TextChoices):
        ON_CHECKOUT = 'ON_CHECKOUT', _('On Checkout (Immediate)')
        ON_CONFIRMATION = 'ON_CONFIRMATION', _('On Confirmation (Verified)')

    site_name = models.CharField(max_length=255, default="My Bookshop")
    tracking_trigger = models.CharField(
        max_length=20,
        choices=TrackingTrigger.choices,
        default=TrackingTrigger.ON_CHECKOUT,
        help_text="When should the Purchase pixel event be fired?"
    )

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
