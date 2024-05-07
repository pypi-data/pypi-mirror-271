from django.db import models
import datetime
import random
import string
from django.utils import timezone
# Create your models here.

class VerificationToken(models.Model):
    def gen_rnd_key():
        return "".join(random.sample(string.digits, 5))

    owner = models.ForeignKey("authsystem.User", models.CASCADE)
    key = models.CharField(max_length=5, default=gen_rnd_key)
    delta = datetime.timedelta(minutes=15)
    expire_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.expire_date = timezone.now() + self.delta
        super().save(*args, **kwargs)

    def is_token_expired(self):
        if timezone.now() > self.expire_date:
            return True
        return False

class CellphoneVerificationToken(models.Model):
    def gen_rnd_key():
        return "".join(random.sample(string.digits, 5))

    cellphone = models.CharField(max_length=30)
    key = models.CharField(max_length=5, default=gen_rnd_key)
    delta = datetime.timedelta(minutes=15)
    expire_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.expire_date = timezone.now() + self.delta
        super().save(*args, **kwargs)
    
    def is_token_expired(self):
        if timezone.now() > self.expire_date:
            return True
        return False
