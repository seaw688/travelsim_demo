from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, BooleanFilter, CharFilter
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
import datetime

from api.views import CustomPagination, prepare_paginated_response
from api.views import custom_api_response
from api.utils import ERROR_API
from common.models import LanguageFile
from .serializers import LanguageFileSerializer,LanguageFileCreateSerializer

class LanguageView(generics.ListAPIView,generics.CreateAPIView):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('title', )

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            serializer_class = LanguageFileCreateSerializer
            return serializer_class
        else:
            serializer_class = LanguageFileSerializer

            return  serializer_class

    def get_queryset(self):
            queryset =  LanguageFile.objects.all()
            return queryset



    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        queryset = self.filter_queryset(queryset)

        if queryset.exists():
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset,many=True,context={"request": request})
            return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

        else:
            error = {"detail": ERROR_API['125'][1]}
            error_codes = [ERROR_API['125'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)


    def create(self, request, *args, **kwargs):
        if self.request.user.role != 'ADMIN' and self.request.user.role != 'MANAGER':
            error = {"detail": ERROR_API['117'][1]}
            error_codes = [ERROR_API['117'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)


        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            error = {"detail": ERROR_API['200'][1]}
            error_codes = [ERROR_API['200'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_200_OK)



        else:

            error = {"detail": ERROR_API['400'][1]}
            error_codes = [ERROR_API['400'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)


class LanguageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LanguageFile.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), ]


    def get_serializer_class(self):
        if self.request.method == 'POST':
            serializer_class = LanguageFileCreateSerializer
            return serializer_class

        if self.request.method == 'PATCH':
            serializer_class = LanguageFileCreateSerializer
            return serializer_class

        serializer_class = LanguageFileSerializer
        return serializer_class



    def retrieve(self, request, *args, **kwargs):
        object = self.get_object()
        serializer_class = self.get_serializer_class()

        if object != None:
            serializer = serializer_class(instance=object,context={"request": request})
            return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

        else:
            error = {"detail": ERROR_API['125'][1]}
            error_codes = [ERROR_API['125'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        if self.request.user.role != 'ADMIN' and self.request.user.role != 'MANAGER':
            error = {"detail": ERROR_API['117'][1]}
            error_codes = [ERROR_API['117'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        object = self.get_object()
        if object != None:
            object.delete()
            error = {"detail": ERROR_API['200'][1]}
            error_codes = [ERROR_API['200'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_200_OK)

        else:
            error = {"detail": ERROR_API['125'][1]}
            error_codes = [ERROR_API['125'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        if self.request.user.role != 'ADMIN' and self.request.user.role != 'MANAGER':
            error = {"detail": ERROR_API['117'][1]}
            error_codes = [ERROR_API['117'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        serializer_class = self.get_serializer_class()

        object = self.get_object()

        if object != None:
            serializer = serializer_class(instance=object,data=request.data,partial=True,context={"request": request})
            if serializer.is_valid():
                serializer.save()
                error = {"detail": ERROR_API['200'][1]}
                error_codes = [ERROR_API['200'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_200_OK)
            else:
                error = {"detail": ERROR_API['400'][1]}
                error_codes = [ERROR_API['400'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            error = {"detail": ERROR_API['125'][1]}
            error_codes = [ERROR_API['125'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

