from rest_framework import status, views, permissions, generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import OTP
import random

User = get_user_model()

class SendOTPView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate 4 digit OTP
        otp_code = str(random.randint(1000, 9999))

        # Save to DB
        OTP.objects.create(phone_number=phone_number, code=otp_code)

        # In a real app, integrate with SMS Gateway here
        print(f"DEBUG: OTP for {phone_number} is {otp_code}")

        return Response({'message': 'OTP sent successfully', 'debug_otp': otp_code})

class VerifyOTPView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp_code = request.data.get('otp')

        if not phone_number or not otp_code:
            return Response({'error': 'Phone number and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify OTP from DB
        otp_obj = OTP.objects.filter(phone_number=phone_number, code=otp_code, is_verified=False).last()

        if otp_obj and otp_obj.is_valid():
            # OTP Verified
            otp_obj.is_verified = True
            otp_obj.save()

            # Get or Create User
            user, created = User.objects.get_or_create(phone_number=phone_number)
            if created:
                user.set_unusable_password() # If logging in via OTP without password
                user.save()

            # Generate JWT
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
                'is_new_user': created
            })
        else:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
