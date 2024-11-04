import json
import requests
import os
from utils.services import AuthService

# def validate(request):
#     token = request.COOKIES.get('jwt')
#     if not token:
#         print("hi im here................")
        
#         return None, ('missing credentials', 401)
#     print("hi im here................")
#     response = AuthService.post('validate/', data={'jwt':token})
#     if response.status_code == 200:
#         return response.json(), None
#     else:
#         return None, (response, response.status_code)


def validate(request):
    token = request.headers.get('Authorization')
    if not token:
        return None, ('missing credentials', 401)

    token = token.split(' ')[1] if ' ' in token else token
    response = AuthService.post('validate/', data={'jwt': token})
    if response.status_code == 200:
        return response.json(), None
    else:
        return None, (response, response.status_code)