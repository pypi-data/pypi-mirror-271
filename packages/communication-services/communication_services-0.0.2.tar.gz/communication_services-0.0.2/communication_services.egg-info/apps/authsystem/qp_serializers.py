from django.utils.translation import gettext as _
from rest_framework import serializers
import logging
from django.shortcuts import get_object_or_404
from . import models
logger = logging.getLogger(__name__)


class SyncUserQpSerializer(serializers.Serializer):
    email = serializers.EmailField(required = False)
    cellphone = serializers.CharField(required = False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial_data.get('cellphone'):
            self.fields.pop('email')
        elif self.initial_data.get('email'):
            self.fields.pop('cellphone')

    def validate_email(self , email):
        if not hasattr(self , 'queryset'):
            self.queryset = self.get_queryset()
        try:
            user = self.queryset.get(email=email)
        except models.User.DoesNotExist:
            raise serializers.ValidationError(_("User with this email does not exists."))
        return user

    def validate_cellphone(self , cellphone):
        if not hasattr(self , 'queryset'):
            self.queryset = self.get_queryset()
        try:
            user = self.queryset.get(cellphone=cellphone)
        except models.User.DoesNotExist:
            raise serializers.ValidationError(_("User with this cellphone does not exists."))
        user = get_object_or_404(self.queryset , cellphone = cellphone)
        return user

    def validate(self , data):
        if not data.get('cellphone') and not data.get('email'):
            raise serializers.ValidationError(_("Either specify user's cellphone or email."))
        return data

    def get_queryset(self):
        return self.context['org'].user_set.all()

    def to_representation(self, instance):
        rep = {'user': None}
        if instance.get('email'):
            rep['user'] = instance.get('email')
        if instance.get('cellphone'):
            rep['user'] = instance.get('cellphone')
        return rep
