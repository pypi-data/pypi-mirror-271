from django.db import models
from django.utils import timezone

from apps.communication.app_models.types_models.public_types_models import STATUS_CHOICES,SMS_TYPE_CHOICES

class smsNotification(models.Model):
    recipient_phone = models.CharField(max_length=20)
    message = models.TextField()
    type =models.CharField(max_length=3, choices=SMS_TYPE_CHOICES.choices, default=SMS_TYPE_CHOICES.CHOICE_SMS)
    status=models.CharField(max_length=4, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.CHOICE_PENDING)
    status_msg= models.CharField(default=None,null=True,max_length=255)
    sendDate = models.DateTimeField(default=None,null=True) 
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Sms Notification "
