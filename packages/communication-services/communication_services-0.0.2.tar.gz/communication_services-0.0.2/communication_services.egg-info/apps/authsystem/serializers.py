from rest_framework import serializers
import logging
from authsystem import models as auth_models
import re
from rest_framework.exceptions import APIException
from . import utils
from django.contrib.auth.password_validation import validate_password
import django.core.exceptions as django_exc
from django.utils.translation import gettext as _
from rest_framework.settings import api_settings
from rest_framework.validators import UniqueValidator

logger = logging.getLogger(__name__)


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_models.User
        fields = ["id", "username", "cellphone", "fullname", "email", "avatar"]
        read_only_fields = ["id", "username"]

    def update(self, instance, validated_data):
        """fields that could be updated are as follows:
        cellphone
        email
        fullname
        """
        for key, value in validated_data.items():
            setattr(instance, key, value)

        try:
            instance.save()
        except:
            logger.exception(
                f"FAILED TO UPDATE USER:{self.context['view'].request.user}"
            )
            raise APIException
        return instance


class RegisterSerializer(UserBaseSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = auth_models.User
        fields = ["id", "username", "email", "cellphone", "fullname", "token", "avatar"]
        extra_kwargs = {
            "fullname": {"required": True, "allow_blank": False},
            "cellphone": {"required": True},
        }

    def get_token(self, obj):
        return self.token.key

    def create(self, validated_data):
        try:
            self.user_obj = super().create(validated_data)
        except:
            logger.exception(
                f"FAILED TO Register USER  WITH USERNAME <{validated_data.get('username')}>"
            )
            raise APIException
        else:
            self.token = utils.create_token(self.user_obj)
        return self.user_obj


class LoginSerializer(serializers.Serializer):
    verify_token = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        errors = {}
        try:
            validate_password(data.get("new_password"))
        except django_exc.ValidationError as e:
            errors["new_password"] = e.messages
        if data.get("old_password") == data.get("new_password"):
            errors[api_settings.NON_FIELD_ERRORS_KEY] = _(
                "new password should be different than old ones."
            )
        if errors:
            raise serializers.ValidationError(errors)
        return data


class ResetPasswordSerializer(serializers.Serializer):
    key = serializers.CharField(required=True, allow_null=False)
    new_password = serializers.CharField(required=True, allow_null=False)

    def validate(self, data):
        errors = {}
        try:
            validate_password(data.get("new_password"))
        except django_exc.ValidationError as e:
            errors["new_password"] = e.messages
            raise serializers.ValidationError(errors)
        return data
