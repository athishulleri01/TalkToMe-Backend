import os
from django.http import HttpResponseBadRequest
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.services import AuthService 
from utils.authorization import validate

class RegisterUserView(APIView):
    def post(self, request):
        if request.method == 'POST':
            response = AuthService.post('register/',data=request.data)
            
            print("register responce:::::::::::::::::::::::::::::::",response)
            return Response(response.json(), status=response.status_code)
    

class LoginView(APIView):
    def post(self, request):
        response = AuthService.post('login/',data=request.data)
        
        print(response)
        if response.status_code == 201 or response.status_code == 200:
            auth_response = response.json()
            token = auth_response.get('jwt', None)
            print("tookkk...............")
            print(token)
            if token:
        #         # Include the entire payload from auth service in the response
                response = Response(auth_response)
                response.set_cookie(key='jwt', value=token, httponly=True)
                print(response.data)
                return response
            response_data = response.json()
            return Response(response_data, status=response.status_code)
        else:
            response_data = response.json()
            return Response(response_data, status=response.status_code)

                
        
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'logged out successfully'
        }
        return response 
   
    
class OTPVerification(APIView):
    def post(self, request):
        if request.method == 'POST':
            response = AuthService.post('verify-otp/', data=request.data)
            print("otp response:::::::::::::::::::::::::::::::", response)
            
            try:
                if response.status_code==200:
                    response_data = response.json()
                    print("respomce",response_data)
                else:
                    return Response({'message': 'Invalid response from AuthService'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except ValueError:
                return Response({'message': 'Invalid response from AuthService'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                        'message': 'OTP varification successfully'
                    }, status=status.HTTP_200_OK)


class OTPResend(APIView):
    def post(self, request):
       
        response = AuthService.post('otp/resend/', data=request.data)
        try:
            if response.status_code==200:
                response_data = response.json()
            else:
                return Response({'message': 'Invalid response from AuthService'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError:
            return Response({'message': 'Invalid response from AuthService'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
                    'message': 'OTP resend successfully'
                }, status=status.HTTP_200_OK)


class ApiTesting(APIView):
    def post(self, request):
        auth_service_url = "http://auth-service:8000/api/api-test/"  # Ensure URL path matches

        try:
            response = requests.post(auth_service_url, json=request.data)
            response.raise_for_status()  # Raises an error for bad status codes

            # Attempt to parse the response as JSON
            response_data = response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return Response({'error': str(http_err)}, status=response.status_code)
        except Exception as err:
            print(f"Other error occurred: {err}")
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response_data, status=response.status_code)
    
    
    
class TokenVerify(APIView):
    def post(self, request):
        response = AuthService.post('token/verify/',data=request.data)
        if response.status_code == 201 or response.status_code == 200:
            response_data = response.json()
            return Response(response_data, status=response.status_code)
        else:
            response_data = response.json()
            return Response(response_data, status=response.status_code)
        

class TokenRefresh(APIView):
    def post(self, request):
        response = AuthService.post('token/refresh/',data=request.data)
        if response.status_code == 201 or response.status_code == 200:
            response_data = response.json()
            return Response(response_data, status=response.status_code)
        else:
            response_data = response.json()
            return Response(response_data, status=response.status_code)
        
        
class ChangePasswordView(APIView):
     def post(self,request):
        response = AuthService.post('change-password/',data=request.data)
        if response.status_code == 201 or response.status_code == 200:      
            response_data = response.json()
            return Response(response_data, status=response.status_code)
        else:
            response_data = response.json()
            return Response(response_data, status=response.status_code)
        
        
class UserView(APIView):
    def get(self, request,id):
        payload, err = validate(request)
        if err:
            return Response({'error': err}, status=status.HTTP_401_UNAUTHORIZED)
        if payload and payload["role"]=='user':
            headers = {
                'Authorization': request.headers.get('Auth'),
            }
            print("headers",headers)
            response = AuthService.get(f"user/info/{id}", headers=headers)
            if response.status_code == 200:
                return Response(response.json(), status=response.status_code)
            else:
                return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
    def put(self, request,id):
        payload, err = validate(request)
        if err:
            return Response({'error': err}, status=status.HTTP_401_UNAUTHORIZED)
        if payload and payload["role"]=='user':
            headers = {
                'Authorization': request.headers.get('Auth'),
            }
            # print("request.data",request.data)
            response = AuthService.put(f"user/info/{id}",data= request.data, headers=headers)
            if response.status_code == 200:
                return Response(response.json(), status=response.status_code)
            else:
                return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        