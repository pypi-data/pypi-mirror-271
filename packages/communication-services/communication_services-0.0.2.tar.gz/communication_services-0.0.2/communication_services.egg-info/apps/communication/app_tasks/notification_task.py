from celery import shared_task
from django.utils import timezone  # Import timezone from django.utils

from apps.communication.app_models.interfaces.main_interface import db_update
from ..app_models.models import mobileNotification,STATUS_CHOICES
from firebase_admin import messaging

@shared_task
def send_notification_task(token, title, body,db_id,image_url=None, data=None):
    currentdate= timezone.now()
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body, image=image_url),
        token=token,
        data=data  # Additional data to be sent in the message
    )
    response = messaging.send(message)
    if response:
        db_update(mobileNotification, instance_id=db_id, status=STATUS_CHOICES.CHOICE_SEND,sendDate=currentdate)
    else:
        db_update(mobileNotification, instance_id=db_id, status=STATUS_CHOICES.CHOICE_UNSEND,sendDate=None)
    return response
