from rest_framework.authtoken.models import Token
import logging
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


def create_token(user):
    return Token.objects.create(user=user)


def revoke_token(user):
    token = Token.objects.filter(user=user)
    if token.exists():
        token.delete()
    return create_token(user)
