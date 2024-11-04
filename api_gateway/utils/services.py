import os, requests
from decouple import config

class AuthService:
    # endpoint = os.getenv('AUTH_SERVICE_URL') + '/api/'
    # endpoint = 'http://auth-service:8000/api/'
    endpoint = config("AUTH_SERVICE_URL", default="") + 'api/'

    @staticmethod
    def get(path, **kwargs):
        headers = kwargs.get('headers', [])
        return requests.get(AuthService.endpoint + path, headers=headers)

    @staticmethod
    def post(path, **kwargs):
        headers = kwargs.get('headers', [])
        data = kwargs.get('data', [])
        return requests.post(AuthService.endpoint + path, data=data, headers=headers)

    @staticmethod
    def put(path, **kwargs):
        headers = kwargs.get('headers', [])
        data = kwargs.get('data', [])
        return requests.put(AuthService.endpoint + path, data=data, headers=headers)

    @staticmethod
    def patch(path, **kwargs):
        headers = kwargs.get('headers', [])
        data = kwargs.get('data', [])
        return requests.patch(AuthService.endpoint + path, data=data, headers=headers)