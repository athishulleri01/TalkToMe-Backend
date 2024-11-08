# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook')
]
