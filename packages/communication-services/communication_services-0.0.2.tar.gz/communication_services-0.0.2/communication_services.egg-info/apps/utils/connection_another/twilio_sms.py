from numbers import Number
from twilio.rest import Client
from django.conf import settings
from django.db import models

class TWILIO_CHAENL_CHOICES(models.TextChoices):
    CHOICE_SMS = 'sms', 'SMS'
    CHOICE_MMS = 'mms', 'MMS'
    CHOICE_WHATSAPP = 'whatsapp', 'WhatsApp'
    CHOICE_VOICE = 'voice', 'Voice'
    CHOICE_EMAIL = 'email', 'Email'
    CHOICE_ERROR = 'error', ("Error")
    
# Send SMS message
def twilio_send_sms(recipient_number, message):
    # Initialize Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Send SMS message
    try:
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=recipient_number
        )
        return True, message.sid
    except Exception as e:
        return False, str(e)

# create service for send verification Code
# return: service Id for send verify_sms
def twilio_create_verify_service(friendly_name:str,code_length:Number,channel:TWILIO_CHAENL_CHOICES=TWILIO_CHAENL_CHOICES.CHOICE_SMS):
    try:
        # Your Twilio Account SID and Auth Token from twilio.com/console
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # create service for send verification Code
        verification = client.verify.services.create(
            friendly_name=friendly_name,
            code_length=code_length,
            channel= channel
        )
        return True,verification.sid
    except Exception as e:
        return False, str(e)
    
# Send verification code
# return: service Id for send verify_sms
def twilio_send_token_verify_service(recipient_phone_number,service_id:str=settings.TWILIO_VERIFY_SID,channel:TWILIO_CHAENL_CHOICES=TWILIO_CHAENL_CHOICES.CHOICE_SMS):
    try:
        # Your Twilio Account SID and Auth Token from twilio.com/console
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # Send verification code
        verification = client.verify.services(service_id).verifications.create(
            to=recipient_phone_number,
            channel=channel
        )

        return True,verification.sid
    except Exception as e:
        return False, str(e)

# Verify the code entered by the user
# return value :
#    The verification_check.status returned by the Twilio Verify API can have the following values:
#    pending: The verification is pending, meaning the verification code has been sent but has not yet been verified by the user.
#    approved: The verification is approved, meaning the verification code entered by the user matches the one sent by Twilio.
#    canceled: The verification is canceled, meaning the verification process was canceled before completion.
#    expired: The verification has expired, meaning the verification code sent by Twilio has expired and is no longer valid.
#    failed: The verification has failed, meaning the verification code entered by the user does not match the one sent by Twilio.
#    pending_code_generation: Twilio is still generating the verification code for this request.
#    error = error 500 in code 
def twilio_check_token_verify_service(recipient_phone_number,code,service_id:str=settings.TWILIO_VERIFY_SID):
    try:
        # Your Twilio Account SID and Auth Token from twilio.com/console
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # Verify the code entered by the user
        verification_check = client.verify.services(service_id) \
            .verification_checks.create(to=recipient_phone_number, code=code)

        return True,verification_check.status
    except Exception as e:
        print(str(e))
        return False,'error'