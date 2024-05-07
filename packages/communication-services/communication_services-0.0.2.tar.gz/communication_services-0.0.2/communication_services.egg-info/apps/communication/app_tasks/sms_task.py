from celery import shared_task
from django.conf import settings
from django.utils import timezone  # Import timezone from django.utils

from apps.communication.app_models.interfaces.main_interface import db_update
from apps.utils.connection_another.twilio_sms import TWILIO_CHAENL_CHOICES, twilio_check_token_verify_service, twilio_send_sms, twilio_send_token_verify_service
from ..app_models.models import smsNotification,STATUS_CHOICES

@shared_task
def send_sms_notification_task(number, message,db_id):
    try:
        # Example usage:
        success, message_sid = twilio_send_sms(number, message)
        currentdate= timezone.now()
        if success:
            db_update(smsNotification, instance_id=db_id, status=STATUS_CHOICES.CHOICE_SEND,sendDate=currentdate)
        else:
            db_update(smsNotification, instance_id=db_id, status=STATUS_CHOICES.CHOICE_UNSEND,sendDate=None)
        return success, message_sid
    except Exception as e:
        obj = db_update(smsNotification, instance_id=db_id, status=STATUS_CHOICES.CHOICE_ERROR,sendDate=None)
        return False, -1

@shared_task
def send_verify_token_task(number,db_id,service_id=settings.TWILIO_VERIFY_SID):
    try:
        # Example usage:
        success, message_sid = twilio_send_token_verify_service(number,service_id)
        currentdate= timezone.now()
        if success:
            db_update(smsNotification, instance_id=db_id, status=STATUS_CHOICES.CHOICE_SEND,sendDate=currentdate)
        else:
            db_update(smsNotification, instance_id=db_id, status=STATUS_CHOICES.CHOICE_UNSEND,sendDate=None)
        return success, message_sid
    except Exception as e:
        obj = db_update(smsNotification, instance_id=db_id, status=STATUS_CHOICES.CHOICE_ERROR,sendDate=None)
        return False, -1


@shared_task
def check_verify_token_task(number,code,service_id=settings.TWILIO_VERIFY_SID):
    try:
        # Example usage:
        success, message_status = twilio_check_token_verify_service(number,code,service_id)
        return success, message_status
    except Exception as e:
        return False, -1