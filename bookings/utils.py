from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings

def send_booking_email(subject, message, to_email):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])

def send_sms(body, to):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    from_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)
    client.messages.create(body=body, from_=from_number, to=to)
