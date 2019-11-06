import sys
sys.path.append("..")

from rest_framework import serializers

from django.apps import apps
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class MultipartM2MField(serializers.Field):
    def to_representation(self, obj):
        return obj.values_list('id', flat=True).order_by('id')

    def to_internal_value(self, data):
        if isinstance(data, list):
            return data if len(data) > 0 else None
        else:
            data = data.strip('[]')
            return data.split(',') if data else None





