from rest_framework.response import Response
import requests
from utils.authorization import validate
from rest_framework.views import APIView
from rest_framework import status
from utils.services import AuthService


class UserAdminListView(APIView):
    def get(self, request):
        payload, err = validate(request)
        if payload and payload["role"]=='admin':
            response = AuthService.get(f"admin/user/all/")

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        


class UserAdminToggleBlockView(APIView):
    def patch(self, request, id):
        payload, err = validate(request)
        if payload and payload["role"]=='admin':
            response = AuthService.patch(f"admin/user/block/{id}/")
        if response.status_code == 200:
            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
