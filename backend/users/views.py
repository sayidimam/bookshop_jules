from rest_framework import status, views, permissions, generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
import random

User = get_user_model()

# Mock OTP Storage (In production, use Redis or DB)
OTP_STORAGE = {}

class SendOTPView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate 4 digit OTP
        otp = str(random.randint(1000, 9999))
        OTP_STORAGE[phone_number] = otp

        # In a real app, integrate with SMS Gateway here
        print(f"DEBUG: OTP for {phone_number} is {otp}")

        return Response({'message': 'OTP sent successfully', 'debug_otp': otp})

class VerifyOTPView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        if not phone_number or not otp:
            return Response({'error': 'Phone number and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

        stored_otp = OTP_STORAGE.get(phone_number)

        if stored_otp == otp:
            # OTP Verified
            # Get or Create User
            user, created = User.objects.get_or_create(phone_number=phone_number)
            if created:
                user.set_unusable_password() # If logging in via OTP without password
                user.save()

            # Generate JWT
            refresh = RefreshToken.for_user(user)

            # Clear OTP
            del OTP_STORAGE[phone_number]

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
                'is_new_user': created
            })
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
