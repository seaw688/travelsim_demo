from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from ...views import custom_api_response
from .serializers import CategorySerializer


CategoryModel = apps.get_model('common', 'Category')


class CategoryList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        categories = CategoryModel.objects.all()
        serializer = CategorySerializer(categories, many=True)
        response = Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        return response
