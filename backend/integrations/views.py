from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class SmsWebhookView(APIView):
    """
    Receives SMS from Android Forwarder App (e.g. bKash/Nagad received money SMS)
    """
    def post(self, request, *args, **kwargs):
        # TODO: Implement SMS parsing and verification logic
        data = request.data
        # print("SMS Received:", data)
        return Response({"status": "received", "data": data}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class CourierWebhookView(APIView):
    """
    Receives status updates from Courier API (Pathao/Steadfast)
    """
    def post(self, request, *args, **kwargs):
        # TODO: Implement Courier status update logic
        data = request.data
        # print("Courier Update Received:", data)
        return Response({"status": "received", "data": data}, status=status.HTTP_200_OK)
