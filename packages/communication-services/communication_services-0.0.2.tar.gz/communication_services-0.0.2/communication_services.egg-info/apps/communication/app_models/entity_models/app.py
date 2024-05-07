from django.db import models
from django.utils import timezone
from core.my_settings import AUTH_USER_MODEL
import secrets

def generate_api_key():
    return secrets.token_urlsafe(16)

# class app(models.Model):
#     user =  models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     api_key = models.CharField(max_length=100, unique=True)
#     # api_key =  models.CharField(max_length=16, unique=True, default=lambda: secrets.token_hex(8))
#     api_key = models.CharField(max_length=100, unique=True, default=generate_api_key)

#     email_address=models.CharField(max_length=200)
#     email_pass =models.CharField(max_length=200)
#     firebase_apikey =models.CharField(max_length=500)
#     twilio_apikey =models.CharField(max_length=500)
#     created = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.name