# views.py

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://localhost:3000'  
WEBHOOK_SECRET = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
def create_checkout_session(request):
    try:
        data = request.data
        price_id = data.get('price_id')  
        user_id = data.get('user_id')  
        print(price_id) 
        print(user_id)  
        if not price_id:
            return Response({'error': 'Price ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,  # Use the price_id from the request data
                    'quantity': 1,
                },
            ],
            mode='subscription',  
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
            subscription_data={
                    'metadata': {
                        'user_id': user_id,
                    }
                }
        )
        print(checkout_session)
        return Response({'checkout_url': checkout_session.url}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def stripe_webhook(request):
    print('webhook')

    payload = request.body
    print(payload)
    # sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print('sig_header',sig_header)
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header,  WEBHOOK_SECRET
        )
    except ValueError as e:
        print('value error')
        return Response({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        print('signatureVerificationError')
        return Response({'error': str(e)}, status=400)

    if event['type'] == 'checkout.session.succeeded':
        payment_intent = event['data']['object']
        handle_payment_intent_succeeded(payment_intent)

    return Response({'success': True})

def handle_payment_intent_succeeded(payment_intent):
    # Extract payment-related information
    print('handling payment success')
    print(payment_intent)
    amount = payment_intent['amount']
    currency = payment_intent['currency']
    # customer_email = payment_intent['charges']['data'][0]['billing_details']['email']
    
    # Extract metadata
    metadata = payment_intent['metadata']
    slot_id = metadata.get('slot_id')
    user_id = metadata.get('user_id')
    print(slot_id)
    print(user_id)
