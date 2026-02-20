from django.db import models
from django.conf import settings
from orders.models import Order

class CourierAccount(models.Model):
    class Provider(models.TextChoices):
        PATHAO = 'PATHAO', 'Pathao Courier'
        STEADFAST = 'STEADFAST', 'Steadfast Courier'
        REDX = 'REDX', 'RedX'
        PAPERFLY = 'PAPERFLY', 'Paperfly'

    name = models.CharField(max_length=100, help_text="e.g. Pathao Main, Pathao Backup")
    provider = models.CharField(max_length=20, choices=Provider.choices)

    # Credentials
    api_key = models.CharField(max_length=255, blank=True)
    secret_key = models.CharField(max_length=255, blank=True)
    client_id = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.provider})"

class CourierConsignment(models.Model):
    """
    Tracks specific consignment details for financial reconciliation.
    """
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='consignment')
    account = models.ForeignKey(CourierAccount, on_delete=models.PROTECT, related_name='consignments')

    consignment_id = models.CharField(max_length=100, db_index=True)
    tracking_code = models.CharField(max_length=100, db_index=True)

    # Financials
    expected_cod = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount courier should collect")
    received_cod = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Amount actually collected")

    actual_courier_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Charge deducted by courier")

    # Payment Status (From Courier to Merchant)
    is_paid_by_courier = models.BooleanField(default=False)
    payment_received_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=50, blank=True) # e.g. Delivered, Returned
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tracking_code} - {self.status}"

class CourierLedger(models.Model):
    """
    Tracks bulk payments received from courier companies (Bank/Bkash).
    """
    account = models.ForeignKey(CourierAccount, on_delete=models.PROTECT, related_name='ledger_entries')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_ref = models.CharField(max_length=100, help_text="Bank Trx ID")

    date_received = models.DateField()
    note = models.TextField(blank=True)

    # Link to multiple consignments covered by this payment
    covered_consignments = models.ManyToManyField(CourierConsignment, related_name='ledger_payments', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.name} - {self.amount} ({self.date_received})"

class CourierDispute(models.Model):
    class Reason(models.TextChoices):
        OVERCHARGE = 'OVERCHARGE', 'Overcharged Delivery Fee'
        LOST_PARCEL = 'LOST_PARCEL', 'Lost Parcel'
        COD_MISMATCH = 'COD_MISMATCH', 'COD Amount Mismatch'
        DAMAGED = 'DAMAGED', 'Damaged in Transit'

    consignment = models.ForeignKey(CourierConsignment, on_delete=models.CASCADE, related_name='disputes')
    reason = models.CharField(max_length=50, choices=Reason.choices)

    claimed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    resolved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    status = models.CharField(max_length=20, default='OPEN', choices=[('OPEN', 'Open'), ('RESOLVED', 'Resolved'), ('REJECTED', 'Rejected')])
    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispute {self.reason} for {self.consignment.tracking_code}"
