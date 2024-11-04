from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AnonymousUser

from .serializers import LoginSerializer, RegisterSerializer, CustomUserSerializer ,ChangePasswordSerializer
from .tasks import send_otp_task
from .utils import generate_and_store_otp, verify_otp
from users.models import CustomUser
import jwt, datetime


import redis
from decouple import config
REDIS_HOST = config('REDIS_HOST', default='localhost')
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
REDIS_DB = config('REDIS_DB', default=0, cast=int)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


# Using Factory Method Pattern to create authentication methods
class AuthMethodFactory:
    @staticmethod
    def get_auth_method(data):
        if 'otp' in data:
            return OTPAuthentication(data)
        else:
            return PasswordAuthentication(data)


# Abstract class for different authentication methods
class AuthenticationMethod:
    def __init__(self, data):
        self.data = data

    def authenticate(self):
        pass


# Concrete class for OTP authentication
class OTPAuthentication(AuthenticationMethod):
    def authenticate(self):
        user_id = self.data.get('user_id')
        otp = self.data.get('otp')
        result = verify_otp(user_id, otp)
        # return result
        if result:
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return user
        return None


# Concrete class for password authentication
class PasswordAuthentication(AuthenticationMethod):
    def authenticate(self):
        email = self.data.get('email')
        password = self.data.get('password')
        return authenticate(email=email, password=password)


@permission_classes([AllowAny])
class Login(APIView):
    def post(self, request):
        data = request.data
        authentication_method = AuthMethodFactory.get_auth_method(data)
        user = authentication_method.authenticate()

        if not user:
            return Response({'status': False, 'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_blocked:
            return Response({'status': False, 'message': 'Your account is blocked'}, status=status.HTTP_403_FORBIDDEN)
        if not user.is_superuser:
            if not user.is_otp_verify:
                # otp = generate_and_store_otp(user.id)
                # print("============", otp, "============ otp")
                # # Sending OTP via Celery task
                # send_otp_task.delay(user.email, otp)
                return Response({'status': False, 'message': 'Your OTP varificatioin not completed, OTP send to your email.' ,'id':user.id}, status=status.HTTP_406_NOT_ACCEPTABLE)
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        payload = {
            'id': user.id,
            'role': user.role,
            'name': user.username,
            'access': access_token,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=600),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
                'id': user.id,
                'jwt':token,
                'refresh': str(refresh),
                'access': access_token,
                'role': user.role,
                'status': True,
            } 
        return response
        # return Response({'status': True, 'token': str(refresh.access_token),'refresh_token': str(refresh),'role':user.role}, status=status.HTTP_200_OK)
    
    


@permission_classes([AllowAny])
class Register(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            user = CustomUser.objects.get(username=user_data['username'])
            user.is_active = True
            user.save()
            # Generating OTP
            otp = generate_and_store_otp(user.id)
            print("============", otp, "============ otp")
            # Sending OTP via Celery task
            send_otp_task.delay(user.email, otp)

            user_info = {
                'user_id': user.id,
                'message': 'User created successfully',
            }

            return Response(user_info, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# @permission_classes([AllowAny])
# class Register(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             # Explicitly create the user instance
#             user_data = serializer.validated_data
#             user = CustomUser.objects.create_user(
#                 username=user_data['username'],
#                 first_name=user_data['first_name'],
#                 last_name=user_data['last_name'],
#                 email=user_data['email'],
#                 phone_number=user_data['phone_number'],
#                 password=user_data['password'],
#                 country=user_data.get('country', ''),
#                 is_paid=user_data.get('is_paid', False),
#                 is_active=True
#             )
#             # genarating otp
#             otp = generate_and_store_otp(user.id)
#             print("============", otp, "============ otp")
#             # sent otp to celery
#             send_otp_task.delay(user.email, otp)
#             # Additional steps as needed (e.g., send confirmation email, etc.)
#             user_info = {
#                 'user_id': user.id,
#                 'message': 'User created successfully',
#                 'datas': str(user.id),
#             }

#             return Response(user_info , status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class OTPVerification(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         stored_otp=0
#         user_id = request.data.get('user_id')
#         otp = request.data.get('otp')
#         stored_otp = redis_client.get(f'otp:{user_id}')
#         authentication_method = AuthMethodFactory.get_auth_method(request.data)
#         user = authentication_method.authenticate()

#         if user:
#             login(request, user)
#             refresh = RefreshToken.for_user(user)
#             return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
#         return Response({'message': 'Invalid OTP','user_id':user_id,'otp':otp,"stored_otp":stored_otp}, status=status.HTTP_400_BAD_REQUEST)




class OTPVerification(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        stored_otp=0
        user_id = request.data.get('user_id')
        otp = request.data.get('otp')
        print(otp,user_id,"........................")
        stored_otp_bytes = redis_client.get(f'otp:{user_id}')
        if stored_otp_bytes is None:
            return Response({
                        'message': 'OTP expired'
                    }, status=status.HTTP_408_REQUEST_TIMEOUT)
        stored_otp = stored_otp_bytes.decode('utf-8')
        print(stored_otp,type(stored_otp),"............",otp,type(otp))
        if stored_otp is not None:
            if otp == stored_otp:
                print("....................")
                user = CustomUser.objects.get(id=user_id)
                # user.is_active = True
                user.is_otp_verify = True
                user.save()
                if user:
                    login(request, user)
                    return Response({
                        'message': 'OTP registration successfully'
                    }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Invalid OTP',
            'user_id': user_id,
            'otp': otp,
            'stored_otp': stored_otp
        }, status=status.HTTP_400_BAD_REQUEST)



class OTPResend(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.is_active = True
        user.save()

        otp = generate_and_store_otp(user_id)
        print("============", otp, "============ otp")
        send_otp_task.delay(user.email, otp)
        return Response({'message': 'Otp resent'}, status=status.HTTP_200_OK)


class ValidateView(APIView):
    def post(self, request):
        # Step 1: Retrieve the token from the request data
        token = request.data.get('jwt')
        
        # Step 2: Check if the token is present
        if not token:
            return Response({'error': 'JWT token not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Step 3: Attempt to decode the token
            print("Received Token: ", token)
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print("payload::::::::::::::::::",payload)
            user = CustomUser.objects.get(id=payload['id'])
            request.user = user
            print("request.user",request.user)
            # If successful, the token is valid and not expired
            return Response(payload)
        
        except jwt.ExpiredSignatureError:
            # Step 4: Handle the case where the token has expired
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except jwt.InvalidTokenError:
            # Step 5: Handle other cases of invalid token
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    
class APIChecker(APIView):
    def post(self, request):
        print("Request Data at auth_service:", request.data)
        return Response({'sucess': 'wellcome'}, status=status.HTTP_200_OK)
    

class ChangePasswordView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print("...................")
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = request.data.get('id')
        print(user_id)
        
        print("...")
        
        try:
            print("...")
            user = CustomUser.objects.get(id=user_id)
            print("user",user)
            print(".......")
            if not user.check_password(serializer.validated_data['current_password']):
                return Response({"detail": "Current password is incorrect.","pass":serializer.validated_data['current_password']}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class UserView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request,id):
        user = CustomUser.objects.get(id=id)
        print("user=====",user)
        if user is None:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request,id):
        user = CustomUser.objects.get(id=id)
        if user is None:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if 'username' in request.data:
            existing_user = CustomUser.objects.filter(username=request.data['username']).exclude(id=user.id).first()
            if existing_user:
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)