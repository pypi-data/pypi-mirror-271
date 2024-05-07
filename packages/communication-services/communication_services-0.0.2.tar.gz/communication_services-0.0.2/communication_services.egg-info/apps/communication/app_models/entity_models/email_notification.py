from django.db import models
from django.utils import timezone

from ..types_models.public_types_models import STATUS_CHOICES


class emailNotification(models.Model):
    recipient_emails = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    status=models.CharField(max_length=4, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.CHOICE_PENDING)
    status_msg= models.CharField(default=None,null=True,max_length=255)
    sendDate = models.DateTimeField(null=True,default=None) 
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Email Notification "
