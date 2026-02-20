from django.db import models
from django.utils.translation import gettext_lazy as _

class Division(models.Model):
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class District(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=100, blank=True)
    lat = models.CharField(max_length=100, blank=True)
    lon = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class ShippingZone(models.Model):
    name = models.CharField(max_length=100, help_text="e.g. Inside Dhaka, Sub Dhaka, Outside Dhaka")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Thana(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=100, blank=True)
    zone = models.ForeignKey(ShippingZone, on_delete=models.SET_NULL, null=True, blank=True, related_name='thanas')

    def __str__(self):
        return self.name

class ShippingRate(models.Model):
    """
    Base tiers: e.g. Up to 0.5kg -> 60tk, Up to 1kg -> 70tk
    """
    zone = models.ForeignKey(ShippingZone, on_delete=models.CASCADE, related_name='rates')
    max_weight = models.DecimalField(max_digits=6, decimal_places=3, help_text="Maximum weight in KG for this rate")
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['max_weight']

    def __str__(self):
        return f"{self.zone} - Up to {self.max_weight}kg: {self.rate}"

class OverweightCharge(models.Model):
    """
    Incremental charge: e.g. Above 1kg, add 20tk per 1kg
    """
    zone = models.ForeignKey(ShippingZone, on_delete=models.CASCADE, related_name='overweight_charges')
    apply_above_weight = models.DecimalField(max_digits=6, decimal_places=3, help_text="Apply this rule if weight is above this value (KG)")
    charge_per_unit = models.DecimalField(max_digits=10, decimal_places=2, help_text="Additional charge per unit weight")
    unit_weight = models.DecimalField(max_digits=6, decimal_places=3, default=1.0, help_text="Unit weight for the additional charge (e.g. 1kg)")

    def __str__(self):
        return f"{self.zone} - Above {self.apply_above_weight}kg: +{self.charge_per_unit}/{self.unit_weight}kg"

class Courier(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=255, blank=True)
    secret_key = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Import split models
from .models_audit import *
from .models_collector import *
