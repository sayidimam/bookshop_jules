from django.urls import path, include
from .views import SendOTPView, VerifyOTPView, UserProfileView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/otp/send/', SendOTPView.as_view(), name='send-otp'),
    path('auth/otp/verify/', VerifyOTPView.as_view(), name='verify-otp'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
]
