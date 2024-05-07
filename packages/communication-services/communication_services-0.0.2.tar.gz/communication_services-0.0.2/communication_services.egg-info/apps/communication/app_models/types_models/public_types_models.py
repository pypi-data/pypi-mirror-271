from django.db import models

class STATUS_CHOICES(models.TextChoices):
    CHOICE_SEND = 'SEND', ("Send")
    CHOICE_UNSEND = 'USND', ("Unsend")
    CHOICE_PENDING = 'PEND', ("Pending")
    CHOICE_ERROR = 'ERRR', ("Error")


class SMS_TYPE_CHOICES(models.TextChoices):
    CHOICE_SMS = 'SMS', ("Sms")
    CHOICE_VERIFY = 'VFY', ("Verify")
    CHOICE_ERROR = 'ERR', ("Error")