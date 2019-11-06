from django.apps import apps
from rest_framework import serializers


CategoryModel = apps.get_model('common', 'Category')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryModel
        fields = ('id', 'category_name', 'parent')