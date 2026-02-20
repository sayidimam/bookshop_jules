from rest_framework import views, status, permissions
from rest_framework.response import Response
from .models import MobilePaymentLog
from .models_parsing import SmsParsingRule
from decimal import Decimal

class SmsWebhookView(views.APIView):
    permission_classes = [permissions.AllowAny] # Usually secured by IP whitelist or secret token

    def post(self, request):
        sender = request.data.get('sender')
        message_body = request.data.get('message')

        if not sender or not message_body:
            return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Find Parsing Rule
        rule = SmsParsingRule.objects.filter(sender_identifier=sender, is_active=True).first()

        if rule:
            extracted_data = rule.parse_message(message_body)
            if extracted_data:
                # 2. Create Log with Extracted Data
                try:
                    amount = Decimal(extracted_data.get('amount', 0))
                    trx_id = extracted_data.get('trx_id')

                    if trx_id:
                        MobilePaymentLog.objects.create(
                            provider=rule.provider_name.upper(), # Or map to enum
                            transaction_id=trx_id,
                            amount=amount,
                            sender_number=extracted_data.get('sender_number', sender), # Extracted or Default
                            reference=extracted_data.get('reference', ''),
                            raw_message=message_body
                        )
                        return Response({'message': 'SMS Parsed and Logged'}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    print(f"Parsing Error: {e}")

        # Fallback: Log Raw Message if no rule matches or parsing fails
        # MobilePaymentLog.objects.create(..., raw_message=message_body)
        # Assuming we only want to log parseable messages for now to avoid junk.

        return Response({'message': 'Received'}, status=status.HTTP_200_OK)
