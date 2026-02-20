import json
import uuid
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from payments.models import MobilePaymentLog, Transaction
from orders.models import Order
from decimal import Decimal

@method_decorator(csrf_exempt, name='dispatch')
class SmsWebhookView(View):
    """
    Receives SMS data from Android Gateway App.
    Expected Payload:
    {
        "sender": "bKash",
        "message": "You have received Tk 500.00 from 017... TrxID 8JHS67...",
        "received_at": "2023-10-25 10:00:00"
    }
    """
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            sender = data.get('sender', '')
            message = data.get('message', '')

            # Simple parsing logic (Regex is better in production)
            provider = MobilePaymentLog.Provider.OTHER
            if 'bKash' in sender or 'bKash' in message:
                provider = MobilePaymentLog.Provider.BKASH
            elif 'Nagad' in sender or 'Nagad' in message:
                provider = MobilePaymentLog.Provider.NAGAD

            # Extract TrxID and Amount (Simplified)
            # In real implementation, use robust regex patterns
            trx_id = None
            amount = 0.00

            parts = message.split()
            if "TrxID" in message:
                for i, part in enumerate(parts):
                    if "TrxID" in part:
                        try:
                            trx_id = parts[i+1]
                        except IndexError:
                            pass
                    if "Tk" in part:
                        try:
                            amount = float(parts[i+1].replace(',', ''))
                        except (ValueError, IndexError):
                            pass

            # Handle unknown or duplicate TrxIDs (e.g. promotional SMS)
            if not trx_id:
                # Generate a unique ID for unparsable messages to avoid DB unique constraint error
                trx_id = f"UNKNOWN-{uuid.uuid4().hex[:8]}"

            # Check if this log already exists (idempotency)
            if MobilePaymentLog.objects.filter(transaction_id=trx_id).exists() and not trx_id.startswith("UNKNOWN"):
                 return JsonResponse({"status": "ignored", "message": "Duplicate TrxID"})

            log = MobilePaymentLog.objects.create(
                provider=provider,
                transaction_id=trx_id,
                amount=amount,
                raw_message=message,
                sender_number=sender # or extract real sender
            )

            # Trigger Auto-Match only if we found a valid TrxID
            if not trx_id.startswith("UNKNOWN"):
                self.match_transaction(log)

            return JsonResponse({"status": "success", "log_id": log.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    def match_transaction(self, log):
        """
        Check if any pending transaction matches this log
        """
        pending_trx = Transaction.objects.filter(
            transaction_id=log.transaction_id,
            status=Transaction.Status.PENDING
        ).first()

        if pending_trx:
            # Verify Amount Tolerance (e.g. +/- 1 taka)
            if abs(pending_trx.amount - Decimal(log.amount)) < 1.0:
                pending_trx.status = Transaction.Status.VERIFIED
                pending_trx.mobile_log = log
                pending_trx.save()

                log.is_claimed = True
                log.save()

                # Update Order Status
                if pending_trx.order:
                    pending_trx.order.status = Order.Status.CONFIRMED # Or whatever status logic
                    pending_trx.order.save()
