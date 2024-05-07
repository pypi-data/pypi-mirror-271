from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from django.utils.translation import gettext as _
import logging
from rest_framework.exceptions import APIException, PermissionDenied
from django.http import Http404
from kavenegar import (
    KavenegarAPI,
    APIException as kavenegar_api_exc,
    HTTPException as kavenegar_http_exc,
)
import re
from . import models

logger = logging.getLogger(__name__)


class CustomPaginationClass(PageNumberPagination):
    page_size_query_param = "page-size"
    max_page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]


class CustomPaginationClass_LargeResult(CustomPaginationClass):
    max_page_size = 500


def err_500_handle(api_job):
    """
    gets an api job  , handle input function erorrs and in case any error occured , pass api job as argument to logger
    """

    def decore2(func):
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except APIException as e:
                # any error that is subclass of APIException , we dont catch it . we raise it.
                raise e
            except Http404 as e:
                raise e
            except:
                logger.exception(f"FAILED TO {api_job.upper()}")
                raise APIException
            else:
                return result

        return inner

    return decore2


class SendSMS:
    def __init__(self, cellphone, token):
        self.cellphone = cellphone
        self.token = token

    def __call__(self):
        self.valid_cellphone(self.cellphone)
        self.send_sms()

    def valid_cellphone(self, string):
        if not re.match("^\+?0?\d*", string):
            logger.exception(f"INVALID CELLPHONE : <{string}>.")
            raise APIException

    def send_sms(self):
        params = {
            "receptor": str(self.cellphone),
            "template": "dgamify-verification",
            "token": self.token,
            "type": "sms",  # sms vs call
        }
        api = KavenegarAPI(apikey=settings.KAVENEGAR_APIKEY)
        try:
            api.verify_lookup(params)
        except (kavenegar_http_exc, kavenegar_api_exc):
            logger.exception(f"FAILED TO SEND SMS TO CELLPHONE: <{self.cellphone}>")
            raise APIException


def create_verification_token(user):
    """this verification token is used in forget password/reset password precedures"""
    if not user:
        raise APIException
    try:
        # we should replace old verifify tokens with new ones if exists.otherwise createing new ones.
        ver_token_obj = models.VerificationToken.objects.get(owner=user)
    except models.VerificationToken.DoesNotExist:
        ver_token_obj = models.VerificationToken.objects.create(owner=user)
    else:
        ver_token_obj.delete()
        ver_token_obj = models.VerificationToken.objects.create(owner=user)
    return ver_token_obj


def create_cellphone_verification_token(cellphone):
    """this verification token is used in get verification code/login precedures"""
    models.CellphoneVerificationToken.objects.filter(
        cellphone=cellphone,
    ).delete()
    ver_token_obj = models.CellphoneVerificationToken.objects.create(
        cellphone=cellphone
    )
    return ver_token_obj
