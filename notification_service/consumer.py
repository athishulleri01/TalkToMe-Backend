import os
import sys
import pika
import json
from decouple import config
from django.core.mail import send_mail
from django.conf import settings

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notification_service.settings")

# Configure Django settings
import django
django.setup()

RABBITMQ_HOST = config('RABBITMQ_HOST', default='localhost')
RABBITMQ_PORT = config('RABBITMQ_PORT', default=5672, cast=int)
RABBITMQ_USERNAME = config('RABBITMQ_USERNAME', default='guest')
RABBITMQ_PASSWORD = config('RABBITMQ_PASSWORD', default='guest')
RABBITMQ_VIRTUAL_HOST = config('RABBITMQ_VIRTUAL_HOST', default='/')

connection_params = pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    virtual_host=RABBITMQ_VIRTUAL_HOST,
    credentials=pika.PlainCredentials(
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD
    )
)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
try:
    # Declare a direct exchange named 'notification_exchange'
    channel.exchange_declare(exchange='notification_exchange', exchange_type='direct')

    # Declare a queue
    channel.queue_declare(queue='login_queue', durable=True)
    channel.queue_bind(exchange='notification_exchange', queue='login_queue', routing_key='login')

    def callback(ch, method, properties, body):
        otp_data = json.loads(body)
        email = otp_data['email']
        print(email)
        otp = otp_data['otp']

        subject = f"Hello, {email}!"
        message = "OTP verification"
        from_email = "your_email@example.com"
        # htmlgen = f"""
        # # HTML content for the email{otp}
        # """
        htmlgen = f"""
#     <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
#   <div style="margin:50px auto;width:70%;padding:20px 0">
#     <div style="border-bottom:1px solid #eee">
#       <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Dryz</a>
#     </div>
#     <p style="font-size:1.1em">Hi,</p>
#     <p>Thank you for choosing TalkToMe. Use the following OTP to complete your Sign Up procedures. OTP is valid for 1 minutes</p>
#     <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2>
#     <p style="font-size:0.9em;">Regards,<br />TalkToMe</p>
#     <hr style="border:none;border-top:1px solid #eee" />
#     <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
#       <p>Dryz</p>
#       <p>contact : 0000000000</p>
#       <p>Email : talktome.official@gamil.com</p>
#     </div>
#   </div>
# </div>
#     """
        send_mail(subject, message, from_email, [email], fail_silently=False, html_message=htmlgen)

    # Set up the callback function for message handling
    channel.basic_consume(queue='login_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for  messages. To exit, press CTRL+C')

    channel.start_consuming()

finally:
    connection.close()



# import pika
# import json
# import pyotp
# from decouple import config
# from decouple import config

# from django.conf import settings
# from django.core.mail import send_mail
# import sys
# import os

# # # Add the root directory to the Python path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# RABBITMQ_HOST = config('RABBITMQ_HOST', default='localhost')
# RABBITMQ_PORT = config('RABBITMQ_PORT', default=5672, cast=int)
# RABBITMQ_USERNAME = config('RABBITMQ_USERNAME', default='guest')
# RABBITMQ_PASSWORD = config('RABBITMQ_PASSWORD', default='guest')
# RABBITMQ_VIRTUAL_HOST = config('RABBITMQ_VIRTUAL_HOST', default='/')

# connection_params = pika.ConnectionParameters(
#     host=RABBITMQ_HOST,
#     port=RABBITMQ_PORT,
#     virtual_host=RABBITMQ_VIRTUAL_HOST,
#     credentials=pika.PlainCredentials(
#         username=RABBITMQ_USERNAME,
#         password=RABBITMQ_PASSWORD
#     )
# )

# connection = pika.BlockingConnection(connection_params)
# channel = connection.channel()
# try:
#     # Declare a direct exchange named 'notification_exchange'
#     channel.exchange_declare(exchange='notification_exchange', exchange_type='direct')

#     # Declare a queue
#     channel.queue_declare(queue='login_queue', durable=True)

#     # Bind the queue to the exchange with the routing key 'login'
#     channel.queue_bind(exchange='notification_exchange', queue='login_queue', routing_key='login')

#     def callback(ch, method, properties, body):
#         otp_data = json.loads(body)
#         email = otp_data['email']
#         otp = otp_data['otp']

#         subject = f"Hello, {email}!"
#         message = "OTP verification"
#         from_email = "your_email@example.com"
#         htmlgen = f"""
#         # HTML content for the email
#         """
#         send_mail(subject, message, from_email, [email], fail_silently=False, html_message=htmlgen)

#     # Set up the callback function for message handling
#     channel.basic_consume(queue='login_queue', on_message_callback=callback, auto_ack=True)

#     print(' [*] Waiting for login messages. To exit, press CTRL+C')
#     channel.start_consuming()

# finally:
#     connection.close()
    
    
    
# # Declare a queue for OTP generation
# channel.queue_declare(queue='notification_exchange', durable=True)

# def callback(ch, method, properties, body):
#     otp_data = json.loads(body)
#     email = otp_data['email']
#     print(email)
#     otp = otp_data['otp']
#     otp_expiry = otp_data['expiry']

#     subject = f"Hello, {email}!"
#     message = "OTP verification"
#     from_email = "dryzz.official@gmail.com"
#     htmlgen = f"""
#     <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
#   <div style="margin:50px auto;width:70%;padding:20px 0">
#     <div style="border-bottom:1px solid #eee">
#       <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Dryz</a>
#     </div>
#     <p style="font-size:1.1em">Hi,</p>
#     <p>Thank you for choosing TalkToMe. Use the following OTP to complete your Sign Up procedures. OTP is valid for 1 minutes</p>
#     <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2>
#     <p style="font-size:0.9em;">Regards,<br />TalkToMe</p>
#     <hr style="border:none;border-top:1px solid #eee" />
#     <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
#       <p>Dryz</p>
#       <p>contact : 0000000000</p>
#       <p>Email : talktome.official@gamil.com</p>
#     </div>
#   </div>
# </div>
#     """
#     send_mail(subject, message, from_email, [email], fail_silently=False, html_message=htmlgen)

# # Set up the callback function for message handling
# channel.basic_consume(queue='notification_exchange', on_message_callback=callback, auto_ack=True)

# print(' [*] Waiting for OTP generation messages. To exit, press CTRL+C')
# channel.start_consuming()
