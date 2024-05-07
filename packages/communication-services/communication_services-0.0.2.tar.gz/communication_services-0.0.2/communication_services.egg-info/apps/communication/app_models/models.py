from django.db import models



# Create your models here.
# from .entity_models.app import app
from .entity_models.mobile_notification import mobileNotification
from .entity_models.email_notification import emailNotification
from .entity_models.sms_notification import smsNotification


#types
from .types_models.public_types_models import STATUS_CHOICES
from .types_models.public_types_models import SMS_TYPE_CHOICES

