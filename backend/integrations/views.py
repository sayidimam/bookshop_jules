import json
import uuid
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from payments.models import MobilePaymentLog, Transaction
from orders.models import Order
from logistics.models_audit import CourierConsignment
from decimal import Decimal

@method_decorator(csrf_exempt, name='dispatch')
class SmsWebhookView(View):
    """
    Receives SMS data from Android Gateway App.
    """
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            sender = data.get('sender', '')
            message = data.get('message', '')

            provider = MobilePaymentLog.Provider.OTHER
            if 'bKash' in sender or 'bKash' in message:
                provider = MobilePaymentLog.Provider.BKASH
            elif 'Nagad' in sender or 'Nagad' in message:
                provider = MobilePaymentLog.Provider.NAGAD

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

            if not trx_id:
                trx_id = f"UNKNOWN-{uuid.uuid4().hex[:8]}"

            if MobilePaymentLog.objects.filter(transaction_id=trx_id).exists() and not trx_id.startswith("UNKNOWN"):
                 return JsonResponse({"status": "ignored", "message": "Duplicate TrxID"})

            log = MobilePaymentLog.objects.create(
                provider=provider,
                transaction_id=trx_id,
                amount=amount,
                raw_message=message,
                sender_number=sender
            )

            if not trx_id.startswith("UNKNOWN"):
                self.match_transaction(log)

            return JsonResponse({"status": "success", "log_id": log.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    def match_transaction(self, log):
        pending_trx = Transaction.objects.filter(
            transaction_id=log.transaction_id,
            status=Transaction.Status.PENDING
        ).first()

        if pending_trx:
            if abs(pending_trx.amount - Decimal(log.amount)) < 1.0:
                pending_trx.status = Transaction.Status.VERIFIED
                pending_trx.mobile_log = log
                pending_trx.save()

                log.is_claimed = True
                log.save()

                if pending_trx.order:
                    pending_trx.order.status = Order.Status.CONFIRMED
                    pending_trx.order.save()

@method_decorator(csrf_exempt, name='dispatch')
class CourierWebhookView(View):
    """
    Scalable endpoint to receive Real-time status updates from Pathao/Steadfast.
    This replaces the need for polling 100k orders.
    """
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Identify Courier (Logic depends on payload structure)
            # Pathao usually sends 'consignment_id', Steadfast 'invoice'

            tracking_code = data.get('consignment_id') or data.get('tracking_code')
            new_status = data.get('order_status') or data.get('status')

            if not tracking_code:
                return JsonResponse({"status": "ignored", "message": "No tracking code found"})

            # Update System
            consignment = CourierConsignment.objects.filter(tracking_code=tracking_code).first()
            if consignment:
                consignment.status = new_status
                consignment.save()

                # Sync with Main Order Status
                if new_status.lower() in ['delivered', 'success']:
                    consignment.order.status = Order.Status.DELIVERED
                    consignment.order.save()
                elif new_status.lower() in ['returned', 'cancelled']:
                    consignment.order.status = Order.Status.RETURNED
                    consignment.order.save()

            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
