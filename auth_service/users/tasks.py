from celery import shared_task
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config

from django.conf import settings
from django.core.mail import send_mail

from auth.rabbitmq_connection import get_rabbitmq_connection
import json

@shared_task
def send_otp_task(email, otp):
    print("jhbjbknkljnkjnknmn")
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        channel.exchange_declare(exchange='notification_exchange', exchange_type='direct')
        user_message = json.dumps({"email": email, "otp": otp})
        routing_key = 'login'
        print("otp : ",otp)
        channel.basic_publish(exchange='notification_exchange', routing_key=routing_key, body=user_message)

        print(f" [x] Sent login message for user '{email}'")
    finally:
        connection.close()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

    # FROM_EMAIL = config('FROM_EMAIL', default='')

    # print("from email ===========", FROM_EMAIL, "==================")

    # subject = 'Your OTP Verification Code'
    # message = f'Your OTP code is: {otp}'
    # from_email = FROM_EMAIL
    # recipient_list = [email]

    # msg = Mail(
    #     from_email=from_email,
    #     to_emails=recipient_list,
    #     subject=subject,
    #     plain_text_content=message
    # )

    # try:
    #     sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    #     response = sg.send(msg)
    #     print(response.status_code)
    #     print(response.body)
    #     print(response.headers)
    # except Exception as e:
    #     print(str(e))
    
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
