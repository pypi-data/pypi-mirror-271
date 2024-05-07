
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone  # Import timezone from django.utils

from apps.communication.app_models.interfaces.main_interface import db_update

from ..app_models.models import emailNotification,STATUS_CHOICES

@shared_task
def send_email_notification_task(subject, message, recipient_list,db_id):
    try:
        currentdate= timezone.now()
        send_mail(subject, message,None, recipient_list)
        db_update(emailNotification,db_id,status=STATUS_CHOICES.CHOICE_SEND,sendDate=currentdate)
    except Exception as e:
        db_update(emailNotification,db_id,status=STATUS_CHOICES.CHOICE_ERROR,status_msg="An error occurred:"+str(e))