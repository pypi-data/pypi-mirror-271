from re import U
from rest_framework import generics
from . import serializers, qp_serializers
from rest_framework.views import Response, APIView
from rest_framework import status
import logging
from django.contrib.auth import authenticate
from . import utils
from django.utils.translation import gettext as _
from rest_framework.permissions import IsAuthenticated
from organization import models as org_models
from utils import helpers, models as utils_models
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    ValidationError,
    PermissionDenied,
    NotFound,
)
from rest_framework.settings import api_settings
from . import models
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


class Register(generics.CreateAPIView):
    def get_serializer_class(self):
        return serializers.RegisterSerializer

    def create(self, request):
        res = super().create(request)
        logger.info(f"user with username <{request.data['username']}> registered")
        return res


class Login(APIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            ver_token_obj = utils_models.CellphoneVerificationToken.objects.get(
                key=serializer.data.get("verify_token")
            )
        except utils_models.CellphoneVerificationToken.DoesNotExist:
            raise AuthenticationFailed
        if ver_token_obj.is_token_expired():
            raise AuthenticationFailed(_("token is expired"))
        try:
            user_obj = models.User.objects.get(cellphone=ver_token_obj.cellphone)
        except models.User.DoesNotExist:
            raise NotFound
        if hasattr(user_obj, "auth_token"):
            token_key = user_obj.auth_token.key
        else:
            try:
                token_key = utils.create_token(user=user_obj).key
            except:
                logger.exception(f"FAILED TO CREATE TOKEN FOR UESR ID:{user_obj.id}")
                raise APIException

        ver_token_obj.delete()
        msg = {
            "token": str(token_key),
            "id": str(user_obj.id),
        }
        return Response(msg, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    serializer_class = serializers.ChangePasswordSerializer

    def patch(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = authenticate(
            username=serializer.data["username"],
            password=serializer.data["old_password"],
        )
        if not user_obj:
            raise AuthenticationFailed
        try:
            user_obj.set_password(serializer.data["new_password"])
            user_obj.save(update_fields=["password"])
            token = utils.revoke_token(user_obj)
            msg = {
                "token": token.key,
                "id": str(user_obj.id),
            }
            return Response(msg, status.HTTP_200_OK)
        except:
            logger.exception(f"AN EXCEPTION OCCURRED FOR USER ID: <{user_obj.id}>.")
            raise APIException


class UserOperation(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return serializers.UserBaseSerializer

    def get_object(self):
        """normally get_object gets object based on `lookedup_field` variable but becouse we want to update her profile , we could get this information through auth token."""
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        self.instance = self.get_object()
        self.perform_logical_destroy()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_logical_destroy(self):
        self.instance.is_deleted = True
        self.instance.save()


class SyncUser(APIView):
    serializer_class = qp_serializers.SyncUserQpSerializer

    @helpers.err_500_handle("sync user")
    def get(self, request, format=None):
        org = self.validate_org_authentication()
        qp_serializer = self.serializer_class(
            data=request.query_params, context={"org": org}
        )
        qp_serializer.is_valid(raise_exception=True)
        user = qp_serializer.data["user"]
        msg = {"id": user.id, "username": user.username, "fullname": user.fullname}
        return Response(msg, status=status.HTTP_200_OK)

    def validate_org_authentication(self):
        api_key = self.request.META.get("HTTP_API_KEY")
        if not api_key:
            raise AuthenticationFailed
        try:
            org = org_models.Organization.objects.get(api_key=api_key)
        except org_models.Organization.DoesNotExist:
            raise AuthenticationFailed
        return org


class ForgetPassword(APIView):
    def get(self, request, format=None):
        cellphone = request.query_params.get("cellphone")
        msg = {"msg": _("we sent verification code to your phone number.")}
        if not cellphone:
            raise ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: [_("cellphone is required")]}
            )
        try:
            user_obj = models.User.objects.get(cellphone=cellphone)
        except models.User.DoesNotExist:
            logger.debug(f"user with cellphone :{cellphone} does not exists")
            # due to sequrity reasons , we wont tell the user that this username exists or not. if we dont do that he can bruteforce the api to request new tokens.
            return Response(msg, status.HTTP_200_OK)
        ver_code = helpers.create_verification_token(user=user_obj).key
        helpers.SendSMS(cellphone=user_obj.cellphone, token=ver_code)()
        return Response(msg, status.HTTP_200_OK)


class ResetPassword(APIView):
    serializer_class = serializers.ResetPasswordSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        ver_token_obj = get_object_or_404(
            utils_models.VerificationToken, key=data.get("key")
        )
        user_obj = ver_token_obj.owner
        if ver_token_obj.is_token_expired():
            raise PermissionDenied(_(f"token expired.try the process again."))
        try:
            user_obj.set_password(data["new_password"])
            user_obj.save(update_fields=["password"])
            token = utils.revoke_token(user_obj)
            ver_token_obj.delete()
        except:
            logger.exception(f"FAILED TO RESET PASSWORD FOR USER <{user_obj.id}>")
            raise APIException

        msg = {
            "token": token.key,
            "id": str(user_obj.id),
        }
        return Response(msg, status.HTTP_200_OK)


class GetCellphoneVerifyToken(APIView):
    def get(self, request, format=None):
        cellphone = request.query_params.get("cellphone")
        msg = {"msg": _("we sent verification code to your phone number.")}
        if not cellphone:
            raise ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: [_("cellphone is required")]}
            )
        ver_code = helpers.create_cellphone_verification_token(cellphone=cellphone).key
        helpers.SendSMS(cellphone=cellphone, token=ver_code)()
        return Response(msg, status.HTTP_200_OK)
