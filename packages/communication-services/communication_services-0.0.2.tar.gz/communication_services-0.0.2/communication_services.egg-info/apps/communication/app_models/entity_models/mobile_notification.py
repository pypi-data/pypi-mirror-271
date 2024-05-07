from django.db import models
from django.utils import timezone

from apps.communication.app_models.types_models.public_types_models import STATUS_CHOICES


class mobileNotification(models.Model):
    recipient = models.CharField(max_length=255)  # Could be a user ID, email, or phone number
    recipient_fcmtoken = models.CharField(max_length=255)  # Could be a user ID, email, or phone number
    title = models.CharField(max_length=255)
    message_text = models.TextField()
    image_url = models.CharField(max_length=255, null=True, blank=True)
    json_data = models.TextField(null=True, blank=True)
    status=models.CharField(max_length=4, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.CHOICE_PENDING)
    status_msg= models.CharField(default=None,null=True,max_length=255)
    sendDate = models.DateTimeField(default=timezone.now, null=True, blank=True) 
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"mobile Notification {self.notification_type.name} - {self.recipient}"