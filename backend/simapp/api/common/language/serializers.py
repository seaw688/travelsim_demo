from django.apps import apps
from rest_framework import serializers
import datetime
from django.utils import timezone
from common.models import LanguageFile
from api.simmarket.simpackage.serializers import SimPackageSerializer



class LanguageFileCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = LanguageFile
        fields = ('id', 'title', 'file')



class LanguageFileSerializer(serializers.ModelSerializer):
    title_full = serializers.CharField(source='get_title_display')
    file_url = serializers.SerializerMethodField()


    class Meta:
        model = LanguageFile
        fields = ('id', 'title','title_full', 'file_url')

    def get_file_url(self, file):
        request = self.context.get('request')
        photo_url = file.file.url
        return request.build_absolute_uri(photo_url)

