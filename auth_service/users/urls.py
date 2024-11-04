from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
# from rest_framework_social_oauth2.views import TokenView, ConvertTokenView, RevokeTokenView

# from .views import Login, Register, OTPVerification, OTPResend, ValidateView
from .views import Login, Register,ValidateView, APIChecker, UserView , OTPVerification, OTPResend, ChangePasswordView

urlpatterns = [
    #Authentication
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),

    #otp
    path('otp/resend/', OTPResend.as_view(), name='otp-resend'),
    path('verify-otp/', OTPVerification.as_view(), name='otp-verification'),

    #Token
    path('validate/', ValidateView.as_view()),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api-test/',APIChecker.as_view(),name='testing'),
    
    path("user/info/<int:id>", UserView.as_view(), name="UserView"),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
    
    
    
