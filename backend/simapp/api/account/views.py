from django.apps import apps
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_auth.models import TokenModel
from api.utils import ERROR_API

from ..views import custom_api_response
from .serializers import ProfileSerializer, ProfilePhotoSerializer, ProfileUpdateSerializer
# from history.utils import history_profile_update_event

ProfileModel = apps.get_model('user_account', 'Profile')
UserModel = get_user_model()


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProfileModel.objects.all()

    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, user_id=None):
        queryset = self.get_queryset()
        if user_id is None:
            obj = get_object_or_404(queryset, user=self.request.user)
        else:
            obj = get_object_or_404(queryset, user_id=user_id)
        return obj

    def retrieve(self, request, user_id=None, *args, **kwargs):
        instance = self.get_object(user_id)
        serializer = self.get_serializer(instance)
        profile_data = serializer.data
        if user_id is None:
            token = TokenModel.objects.filter(user_id=request.user.pk).first()
        else:
            token = TokenModel.objects.filter(user_id=user_id).first()
        profile_data['token'] = str(token)
        return Response(custom_api_response(content=profile_data), status=status.HTTP_200_OK)

    def update(self, request, user_id=None, *args, **kwargs):
        self.serializer_class = ProfileUpdateSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object(user_id)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=False):
            if user_id is None:
                serializer.save(user_id=request.user.pk)
            else:
                serializer.save(user_id=user_id)
            # if getattr(instance, '_prefetched_objects_cache', None):
            #     # If 'prefetch_related' has been applied to a queryset, we need to
            #     # forcibly invalidate the prefetch cache on the instance.
            #     instance._prefetched_objects_cache = {}
            return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        else:
            return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)



from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


class ProfilePhotoView(generics.CreateAPIView,generics.DestroyAPIView):
    queryset = ProfileModel.objects.all()

    serializer_class = ProfilePhotoSerializer
    permission_classes = (IsAuthenticated, )
    allowed_methods = ('POST', )

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    @method_decorator(never_cache)
    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance, serializer.validated_data)
            serializer = self.get_serializer(instance)
            return Response(custom_api_response(content=serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        target = request.data.get('target_field')
        if target:
            instance = self.get_object()
            for x in target:
                if x == 'photo':
                    instance.photo.delete()
                    instance.save()
                elif x == 'airline_image':
                    instance.airline_image.delete()
                    instance.save()
                elif x == 'travel_image':
                    instance.travel_image.delete()
                    instance.save()
                elif x == 'passport_image':
                    instance.passport_image.delete()
                    instance.save()
                elif x == 'medical_image':
                    instance.medical_image.delete()
                    instance.save()
                else:
                    error = {"detail": ERROR_API['125'][1]}
                    error_codes = [ERROR_API['125'][0]]
                    return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)

            ser = self.get_serializer(instance)
            return Response(custom_api_response(content=ser.data), status=status.HTTP_200_OK)

        else:
            error = {"detail": ERROR_API['125'][1]}
            error_codes = [ERROR_API['125'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)



from django.contrib.auth.mixins import AccessMixin
from django_encrypted_filefield.views import FetchView


class MyPermissionRequiredMixin(AccessMixin):
    """
    Your own rules live here
    """
    pass


class MyFetchView(MyPermissionRequiredMixin, FetchView):

    pass