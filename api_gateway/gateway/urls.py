from django.urls import include, path
from .views import RegisterUserView, LoginView, LogoutView, UserView, ApiTesting,TokenVerify, TokenRefresh, UserView, OTPVerification, OTPResend, ChangePasswordView

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/<int:id>/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('api-test/',ApiTesting.as_view()),
    
    path('verify-otp/', OTPVerification.as_view(), name='otp-verification'),
    path('otp/resend/', OTPResend.as_view(), name='otp-resend'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    
    
    
    path('token/verify/',TokenVerify.as_view()),
    path('token/refresh/',TokenRefresh.as_view())
    

]