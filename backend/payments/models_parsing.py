import re
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class SmsParsingRule(models.Model):
    provider_name = models.CharField(max_length=50, help_text="e.g. bKash, Nagad")
    sender_identifier = models.CharField(max_length=50, unique=True, help_text="The SMS Sender ID to match (e.g. 'bKash', '16247')")
    is_active = models.BooleanField(default=True)

    # Regex Configuration
    regex_pattern = models.CharField(
        max_length=500,
        help_text=r"Use named groups for extraction. E.g. TrxID (?P<trx_id>\w+).*Tk (?P<amount>\d+\.\d+)"
    )

    def clean(self):
        try:
            re.compile(self.regex_pattern)
        except re.error as e:
            raise ValidationError(f"Invalid Regex Pattern: {e}")

    def parse_message(self, message_body):
        """
        Returns a dict with keys: transaction_id, amount, sender_number (optional), reference (optional)
        """
        match = re.search(self.regex_pattern, message_body)
        if match:
            return match.groupdict()
        return None

    def __str__(self):
        return f"{self.provider_name} ({self.sender_identifier})"
