from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.contrib.auth import get_user_model

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_auth.models import TokenModel
from rest_auth.app_settings import create_token

from ...views import custom_api_response
from .serializers import CustomUserSerializer, LoginSerializer, UserIsExistsSerializer, RegisterUserSerializer,\
    SocialRegistrationSerializer, SocialAuthSerializer

from ...account.serializers import ProfileSerializer
from account.models import Profile
from common.utils import ROLES

import re
from django.core.files.base import ContentFile
from urllib.parse import urlparse
from urllib.request import urlopen

from ...utils import ERROR_API

from django_rest_passwordreset.views import ResetPasswordRequestToken, ResetPasswordConfirm
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from rest_framework import parsers, renderers, status
from rest_framework.response import Response
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.signals import reset_password_token_created, pre_password_reset, post_password_reset
from django_rest_passwordreset.views import get_password_reset_token_expiry_time

from api.views import CustomPagination, prepare_paginated_response

from api.account.serializers import ProfileSerializerUpdate

User = get_user_model()
UserModel = get_user_model()


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        django_logout(request)

        content = {"detail": "Successfully user logged out"}
        return Response(custom_api_response(None, content), status=status.HTTP_200_OK)


class UserMe(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        serializer = CustomUserSerializer(request.user)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_200_OK)


class UserIsExists(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = UserIsExistsSerializer(data=request.data)
        if serializer.is_valid():
            return Response(custom_api_response(serializer=serializer), status=status.HTTP_200_OK)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering_fields = ('username', 'first_name', 'last_name', 'email','date_joined')
    filter_fields = ('role','is_active' )

    def retrieve(self, request, pk=None):
        user = UserModel.objects.filter(pk=pk).all()
        serializer = self.get_serializer(user, many=True)
        response = Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        return response

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not 'role' in request.GET:
            queryset = queryset.filter(role='CUSTOMER').all()
        queryset = self.filter_queryset(queryset)

        if not queryset.exists():
            error = {"detail": ERROR_API['122'][1]}
            error_codes = [ERROR_API['122'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        paginate = prepare_paginated_response(self, request, queryset)
        if paginate:
            return Response(custom_api_response(content=paginate.content, metadata=paginate.metadata), status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        self_user = request.user
        request.data['creator_id'] = self_user.pk
        if not 'role' in request.data:
            request.data['role'] = 'CUSTOMER'
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        profile_serializer= ProfileSerializerUpdate(instance=user.profile,data=request.data,partial=True)

        if profile_serializer.is_valid(raise_exception=True):
            profile_serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(custom_api_response(serializer=serializer,metadata='sadsaad'), status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        profile_serializer = ProfileSerializerUpdate(instance=instance.profile, data=request.data, partial=True)

        if profile_serializer.is_valid(raise_exception=True):
            profile_serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)



class UserResetPasswordConfirm(ResetPasswordConfirm):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        token = serializer.validated_data['token']

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            # return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)
            error = {"detail": ERROR_API['113'][1]}
            error_codes = [ERROR_API['113'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            # return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)
            error = {"detail": ERROR_API['114'][1]}
            error_codes = [ERROR_API['114'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        # change users password
        if reset_password_token.user.has_usable_password():
            pre_password_reset.send(sender=self.__class__, user=reset_password_token.user)
            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(sender=self.__class__, user=reset_password_token.user)

        # Delete all password reset tokens for this user
        ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

        return Response({'status': 'OK'})


# class UserResetPasswordRequestToken(ResetPasswordRequestToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']
#
#         # before we continue, delete all existing expired tokens
#         password_reset_token_validation_time = get_password_reset_token_expiry_time()
#
#         # datetime.now minus expiry hours
#         now_minus_expiry_time = timezone.now() - timedelta(hours=password_reset_token_validation_time)
#
#         # delete all tokens where created_at < now - 24 hours
#         ResetPasswordToken.objects.filter(created_at__lte=now_minus_expiry_time).delete()
#
#         # find a user by email address (case insensitive search)
#         users = User.objects.filter(email__iexact=email)
#
#         active_user_found = False
#
#         # iterate over all users and check if there is any user that is active
#         # also check whether the password can be changed (is useable), as there could be users that are not allowed
#         # to change their password (e.g., LDAP user)
#         for user in users:
#             if user.is_active and user.has_usable_password():
#                 active_user_found = True
#
#         # No active user found, raise a validation error
#         if not active_user_found:
#             # raise ValidationError({
#             #     'email': ValidationError(
#             #         _("There is no active user associated with this e-mail address or the password can not be changed"),
#             #         code='invalid')}
#             # )
#             error = {"detail": ERROR_API['104'][1]}
#             error_codes = [ERROR_API['104'][0]]
#             return Response(custom_api_response(errors=error, error_codes=error_codes),
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         # last but not least: iterate over all users that are active and can change their password
#         # and create a Reset Password Token and send a signal with the created token
#         for user in users:
#             if user.is_active and user.has_usable_password():
#                 # define the token as none for now
#                 token = None
#
#                 # check if the user already has a token
#                 if user.password_reset_tokens.all().count() > 0:
#                     # yes, already has a token, re-use this token
#                     token = user.password_reset_tokens.all()[0]
#                 else:
#                     # no token exists, generate a new token
#                     token = ResetPasswordToken.objects.create(
#                         user=user,
#                         user_agent=request.META['HTTP_USER_AGENT'],
#                         ip_address=request.META['REMOTE_ADDR']
#                     )
#                 # send a signal that the password token was created
#                 # let whoever receives this signal handle sending the email for the password reset
#                 reset_password_token_created.send(sender=self.__class__, reset_password_token=token)
#         # done
#         return Response({'status': 'OK'})
#
#
# user_reset_password_confirm = UserResetPasswordConfirm.as_view()
# user_reset_password_request_token = UserResetPasswordRequestToken.as_view()


@api_view(['POST'])
@permission_classes(())
def register_view(request):
    # registration handler
    if request.user.is_authenticated == True:
        # "You must have to log out first"
        error = {"detail": ERROR_API['109'][1]}
        error_codes = [ERROR_API['109'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    if 'email' in request.data:
        is_user_exists = UserModel.objects.filter(email=request.data['email']).all()
        if is_user_exists:
            error = {"detail": ERROR_API['103'][1]}
            error_codes = [ERROR_API['103'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        # new_profile_data = {'date_birth': serializer.validated_data['date_birth'] if 'date_birth' in serializer.validated_data else None,
        #                     'phone': serializer.validated_data['phone'] if 'phone' in serializer.validated_data else '',
        #                     'subscribe': serializer.validated_data['subscribe'] if 'subscribe' in serializer.validated_data else False}

        new_profile_data = {'date_birth': serializer.validated_data['date_birth'] if 'date_birth' in serializer.validated_data else None,
                            'phone': serializer.validated_data['phone'] if 'phone' in serializer.validated_data else '',
                            'subscribe': serializer.validated_data['subscribe'] if 'subscribe' in serializer.validated_data else False}

        if 'date_birth' in serializer.validated_data:
            del serializer.validated_data['date_birth']
        if 'phone' in serializer.validated_data:
            del serializer.validated_data['phone']
        if 'subscribe' in serializer.validated_data:
            del serializer.validated_data['subscribe']

        license_number = serializer.validated_data.pop('license_number',None)

        instance = serializer.save()
        if instance.role=='DOCTOR':
            instance.is_active=False
            instance.save()



        instance_id = instance.id
        user_profile = Profile.objects.filter(user_id=instance_id).first()
        profile_serialiser = ProfileSerializer(instance=user_profile, data=new_profile_data)
        if profile_serialiser.is_valid():
            x= profile_serialiser.save()
            x.doctor_license=license_number
            x.save()
        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            token = create_token(TokenModel, user, login_serializer)
            django_login(request, user)
            profile = get_profile_data(user.id, request)
            content = {'token': token.key, 'email': user.email, 'id': user.id, 'first_login': True,
                   'first_name': user.first_name, 'last_name': user.last_name, 'profile': profile, 'role': user.role}
            return Response(custom_api_response(login_serializer, content), status=status.HTTP_200_OK)
        else:
            return Response(custom_api_response(login_serializer), status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes(())
def login_view(request):
    serializer_class = LoginSerializer
    if request.user.is_authenticated == True:
        # "You must have to log out first"
        error = {"detail": ERROR_API['109'][1]}
        error_codes = [ERROR_API['109'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        if user.role == 'CUSTOMER':
            if serializer.validated_data['app'] == 'DOCTOR_APP':
                error = {"detail": ERROR_API['117'][1]}
                error_codes = [ERROR_API['117'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)
        if user.role == "DOCTOR":
            if serializer.validated_data['app'] == 'CUSTOMER_APP':
                error = {"detail": ERROR_API['117'][1]}
                error_codes = [ERROR_API['117'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                    status=status.HTTP_400_BAD_REQUEST)

        token = create_token(TokenModel, user, serializer)
        django_login(request, user)
        profile = get_profile_data(user.id, request)
        content = {'token': token.key, 'email': user.email, 'id': user.id, 'first_login': False,
                   'first_name': user.first_name, 'last_name': user.last_name, 'profile': profile, 'role': user.role}
        return Response(custom_api_response(serializer, content), status=status.HTTP_200_OK)
    else:
        return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)



def get_profile_data(user_id, request=None):
    user_profile = Profile.objects.filter(user_id=user_id).all()
    profile_serializer = ProfileSerializer(instance=user_profile, many=True)
    profile = profile_serializer.data
    if request:
        if profile[0]['photo']:
            profile[0]['photo'] = request.build_absolute_uri(profile[0]['photo'])
        if profile[0]['airline_image']:
            profile[0]['airline_image'] = request.build_absolute_uri(profile[0]['airline_image'])
        if profile[0]['travel_image']:
            profile[0]['travel_image'] = request.build_absolute_uri(profile[0]['travel_image'])
        if profile[0]['passport_image']:
            profile[0]['passport_image'] = request.build_absolute_uri(profile[0]['passport_image'])
    if profile:
        return profile[0]
    else:
        return {}


import facebook
from google.oauth2 import id_token
from google.auth.transport import requests

# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def social_reg_view(request):
#     serializer = SocialRegistrationSerializer(data=request.data)
#
#     if serializer.is_valid():
#         if serializer.validated_data['type']=='GOOGLE':
#             try:
#
#                 token = serializer.validated_data['social_token']
#
#                 try:
#                     idinfo = id_token.verify_oauth2_token(token, requests.Request(),
#                                                           "187369116197-v6ek0vdicnaqnd97t3gnmkq9sgk73eu8.apps.googleusercontent.com")
#                     if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
#                         raise ValueError('Wrong issuer.')
#                 except ValueError:
#                     # "Unable to login via google account, wrong issuer"
#                     error = {"detail": ERROR_API['111'][1]}
#                     error_codes = [ERROR_API['111'][0]]
#                     return Response(custom_api_response(errors=error, error_codes=error_codes),
#                                     status=status.HTTP_400_BAD_REQUEST)
#
#                 last_name = idinfo['family_name']
#                 first_name = idinfo['given_name']
#                 email = idinfo['email']
#                 photo = idinfo['picture']
#                 google_id = idinfo['sub']
#
#                 user = UserModel.objects.get(google_id=google_id)
#                 error = {"detail": ERROR_API['110'][1]}
#                 error_codes = [ERROR_API['110'][0]]
#                 return Response(custom_api_response(errors=error, error_codes=error_codes),
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             except UserModel.DoesNotExist:
#                 token = serializer.validated_data['social_token']
#
#                 try:
#                     idinfo = id_token.verify_oauth2_token(token, requests.Request(),
#                                                           "187369116197-v6ek0vdicnaqnd97t3gnmkq9sgk73eu8.apps.googleusercontent.com")
#                     if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
#                         raise ValueError('Wrong issuer.')
#                 except ValueError:
#                     # "Unable to login via google account, wrong issuer"
#                     error = {"detail": ERROR_API['111'][1]}
#                     error_codes = [ERROR_API['111'][0]]
#                     return Response(custom_api_response(errors=error, error_codes=error_codes),
#                                     status=status.HTTP_400_BAD_REQUEST)
#
#                 last_name = idinfo['family_name']
#                 first_name = idinfo['given_name']
#                 email = idinfo['email']
#                 photo = idinfo['picture']
#                 google_id = idinfo['sub']
#
#                 request.user.google_id = google_id
#                 request.user.save()
#
#                 error = {"detail": ERROR_API['200'][1]}
#                 error_codes = [ERROR_API['200'][0]]
#                 return Response(custom_api_response(errors=error, error_codes=error_codes),
#                                 status=status.HTTP_200_OK)
#
#         if serializer.validated_data['type']=='FACEBOOK':
#             try:
#
#                 access_token = serializer.validated_data['social_token']
#
#                 graph = facebook.GraphAPI(access_token)
#                 args = {'fields': 'id,email,birthday,gender,first_name,last_name,picture.height(500)'}
#                 profile = graph.get_object('me', **args)
#
#                 first_name = profile.get('first_name')
#                 last_name = profile.get('last_name')
#                 gender = profile.get('gender')
#                 birthday = profile.get('birthday')
#                 fb_id = profile.get('id')
#
#
#                 user = UserModel.objects.get(fb_id=fb_id)
#                 error = {"detail": ERROR_API['110'][1]}
#                 error_codes = [ERROR_API['110'][0]]
#                 return Response(custom_api_response(errors=error, error_codes=error_codes),
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             except UserModel.DoesNotExist:
#                 access_token = serializer.validated_data['social_token']
#
#                 graph = facebook.GraphAPI(access_token)
#                 args = {'fields': 'id,email,birthday,gender,first_name,last_name,picture.height(500)'}
#                 profile = graph.get_object('me', **args)
#
#                 first_name = profile.get('first_name')
#                 last_name = profile.get('last_name')
#                 gender = profile.get('gender')
#                 birthday = profile.get('birthday')
#                 fb_id = profile.get('id')
#
#                 request.user.fb_id=fb_id
#                 request.user.save()
#
#                 error = {"detail": ERROR_API['200'][1]}
#                 error_codes = [ERROR_API['200'][0]]
#                 return Response(custom_api_response(errors=error, error_codes=error_codes),
#                                 status=status.HTTP_200_OK)
#
#         else:
#             error = {"detail": ERROR_API['400'][1]}
#             error_codes = [ERROR_API['400'][0]]
#             return Response(custom_api_response(errors=error, error_codes=error_codes),
#                             status=status.HTTP_400_BAD_REQUEST)
#
#
#     else:
#         error = {"detail": ERROR_API['400'][1]}
#         error_codes = [ERROR_API['400'][0]]
#         return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)




#
# @api_view(['POST'])
# @permission_classes(())
# def facebook_auth(request):
#
#     def create_login_token(user):
#         serializer = LoginSerializer()
#         token = create_token(TokenModel, user, serializer)
#         return token
#
#     if request.user.is_authenticated == True:
#         error = {"detail": ERROR_API['109'][1]}
#         error_codes = [ERROR_API['109'][0]]
#         return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)
#
#
#     serializer = SocialAuthSerializer(data=request.data)
#
#     if serializer.is_valid():
#
#         access_token = serializer.validated_data['token']
#
#         graph = facebook.GraphAPI(access_token)
#         args = {'fields': 'id,email,birthday,gender,first_name,last_name,picture.height(500)'}
#         profile = graph.get_object('me', **args)
#
#         fb_id = profile.get('id')
#
#         try:
#             user = UserModel.objects.get(fb_id=fb_id)
#             token = create_login_token(user)
#             profile = get_profile_data(user.id, request)
#             content = {'token': token.key, 'email': user.email, 'id': user.id,
#                        'first_name': user.first_name, 'last_name': user.last_name, 'profile': profile}
#             return Response(custom_api_response(content=content), status=status.HTTP_200_OK)
#
#
#         except UserModel.DoesNotExist:
#             error = {"detail": ERROR_API['110'][1]}
#             error_codes = [ERROR_API['110'][0]]
#             return Response(custom_api_response(errors=error, error_codes=error_codes),
#                             status=status.HTTP_400_BAD_REQUEST)
#
#     else:
#         error = {"detail": ERROR_API['400'][1]}
#         error_codes = [ERROR_API['400'][0]]
#         return Response(custom_api_response(errors=error, error_codes=error_codes),
#                         status=status.HTTP_400_BAD_REQUEST)
#




# @api_view(['POST'])
# @permission_classes(())
# def google_auth(request):
#
#     def create_login_token(user):
#         serializer = LoginSerializer()
#         token = create_token(TokenModel, user, serializer)
#         return token
#
#
#     if request.user.is_authenticated:
#         error = {"detail": ERROR_API['109'][1]}
#         error_codes = [ERROR_API['109'][0]]
#         return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)
#
#
#     serializer = SocialAuthSerializer(data=request.data)
#
#     if serializer.is_valid():
#         token = serializer.validated_data['token']
#
#
#         try:
#             idinfo = id_token.verify_oauth2_token(token, requests.Request(),
#                                                   "187369116197-v6ek0vdicnaqnd97t3gnmkq9sgk73eu8.apps.googleusercontent.com")
#             if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
#                 raise ValueError('Wrong issuer.')
#         except ValueError:
#             error = {"detail": ERROR_API['111'][1]}
#             error_codes = [ERROR_API['111'][0]]
#             return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)
#
#         google_id = idinfo['sub']
#
#         try:
#             user = UserModel.objects.get(google_id=google_id)
#             token = create_login_token(user)
#             profile = get_profile_data(user.id, request)
#             content = {'token': token.key, 'email': user.email, 'id': user.id,
#                        'first_name': user.first_name, 'last_name': user.last_name, 'profile': profile}
#             return Response(custom_api_response(content=content), status=status.HTTP_200_OK)
#
#
#         except UserModel.DoesNotExist:
#             error = {"detail": ERROR_API['120'][1]}
#             error_codes = [ERROR_API['120'][0]]
#             return Response(custom_api_response(errors=error, error_codes=error_codes),
#                             status=status.HTTP_400_BAD_REQUEST)
#
#
#     else:
#         error = {"detail": ERROR_API['400'][1]}
#         error_codes = [ERROR_API['400'][0]]
#         return Response(custom_api_response(errors=error, error_codes=error_codes),
#                         status=status.HTTP_400_BAD_REQUEST)




#
# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def social_unregister_view(request):
#     if request.data['type'] == 'FACEBOOK':
#         request.user.fb_id=''
#         request.user.save()
#         error = {"detail": ERROR_API['200'][1]}
#         error_codes = [ERROR_API['200'][0]]
#         return Response(custom_api_response(errors=error, error_codes=error_codes),
#                         status=status.HTTP_200_OK)
#
#     elif request.data['type'] == 'GOOGLE':
#         request.user.google_id=''
#         request.user.save()
#         error = {"detail": ERROR_API['200'][1]}
#         error_codes = [ERROR_API['200'][0]]
#         return Response(custom_api_response(errors=error, error_codes=error_codes),
#                         status=status.HTTP_200_OK)
#
#     else:
#         error = {"detail": ERROR_API['400'][1]}
#         error_codes = [ERROR_API['400'][0]]
#         return Response(custom_api_response(errors=error, error_codes=error_codes),
#                         status=status.HTTP_400_BAD_REQUEST)
#
#




@api_view(['POST'])
@permission_classes(())
def facebook_auth(request):

    def create_login_token(user):
        serializer = LoginSerializer()
        token = create_token(TokenModel, user, serializer)
        return token

    if request.user.is_authenticated == True:
        error = {"detail": ERROR_API['109'][1]}
        error_codes = [ERROR_API['109'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    access_token = request.data['access_token']

    app = request.data.get('app','CUSTOMER_APP')

    doctor_license = request.data.get('doctor_license',None)

    role = request.data.get('role','CUSTOMER')
    if role !='DOCTOR':
        role = 'CUSTOMER'

    graph = facebook.GraphAPI(access_token)
    args = {'fields': 'id,email,birthday,gender,first_name,last_name,picture.height(500)'}
    profile = graph.get_object('me', **args)

    first_name = profile.get('first_name')
    last_name = profile.get('last_name')
    gender = profile.get('gender')
    birthday = profile.get('birthday')
    email = profile.get('email')
 
    if email == None:
        error = {"detail": ERROR_API['106'][1]}
        error_codes = [ERROR_API['106'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    fb_id = profile.get('id')

    first_login = False

    photo = profile.get('picture',{}).get('data',{}).get('url',{})
    name = urlparse(photo).path.split('/')[-1]+'fb.jpg'
    content = ContentFile(urlopen(photo).read())

    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        try:
             user = UserModel.objects.get(fb_id=fb_id)
             error = {"detail": ERROR_API['110'][1]}
             error_codes = [ERROR_API['110'][0]]
             return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)
        except UserModel.DoesNotExist:
            user = UserModel(email=email, last_name=last_name, first_name=first_name, fb_id=fb_id)
            user.role = role
            if user.role == 'DOCTOR':
                user.is_active=False
                user.save()
                user.profile.doctor_license=doctor_license
                user.save()
            else:
                user.is_active=True
            user.save()
            user.profile.photo.save(name,content,save=True)
            user = UserModel.objects.get(email=email)
            token = create_login_token(user)
            user.last_login = timezone.now()
            user.save()

    if user.fb_id == fb_id:
        if user.is_active != True:
            error = {"detail": ERROR_API['123'][1]}
            error_codes = [ERROR_API['123'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)
        if user.last_login == None:
            first_login = True

        if user.role == 'CUSTOMER':
            if app == 'DOCTOR_APP':
                error = {"detail": ERROR_API['117'][1]}
                error_codes = [ERROR_API['117'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)
        if user.role == "DOCTOR":
            if app == 'CUSTOMER_APP':
                error = {"detail": ERROR_API['117'][1]}
                error_codes = [ERROR_API['117'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)


        token = create_login_token(user)
        user.last_login=timezone.now()
        user.save()
        profile = get_profile_data(user.id, request)
        content = {'token': token.key, 'email': user.email, 'id': user.id, 'first_login': first_login,
                   'first_name': user.first_name, 'last_name': user.last_name, 'profile': profile,'doctor_license':user.profile.doctor_license}
        return Response(custom_api_response(content=content), status=status.HTTP_200_OK)
    else:
        error = {"detail": ERROR_API['120'][1]}
        error_codes = [ERROR_API['120'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes(())
def google_auth(request):
    if request.user.is_authenticated:
        # "You must have to log out first"
        error = {"detail": ERROR_API['109'][1]}
        error_codes = [ERROR_API['109'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    token=request.data['id_token']

    app = request.data.get('app','CUSTOMER_APP')
    doctor_license = request.data.get('doctor_license',None)


    role = request.data.get('role', 'CUSTOMER')
    if role != 'DOCTOR':
        role = 'CUSTOMER'

    try:
        idinfo = id_token.verify_token(token, requests.Request())

        if idinfo['aud'] not in ["187369116197-gv3k031vrs0ttop0bns76b9p1jvmk4tp.apps.googleusercontent.com",
                                 "187369116197-v6ek0vdicnaqnd97t3gnmkq9sgk73eu8.apps.googleusercontent.com",
                                 '187369116197-mc1sbkhi6mbfthag50qlrkmlldqal6sl.apps.googleusercontent.com',
                                 '210803069555-n9vkfohd265n503eg8jibu8g9ds487bq.apps.googleusercontent.com']:
            raise ValueError('Wrong issuer.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            print(idinfo)

            raise ValueError('Wrong issuer.')
    except ValueError:
        # "Unable to login via google account, wrong issuer"

        error = {"detail": ERROR_API['111'][1]}
        error_codes = [ERROR_API['111'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    last_name = idinfo['family_name']
    first_name = idinfo['given_name']
    email = idinfo['email']
    photo = idinfo['picture']
    google_id = idinfo['sub']

    first_login = False

    photo = re.sub(r'/s\d\d-c/',r'/s500-c/',photo)
    name = urlparse(photo).path.split('/')[-1]
    content = ContentFile(urlopen(photo).read())

    def create_login_token(user):
        serializer = LoginSerializer()
        token = create_token(TokenModel, user, serializer)
        return token

    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        try:
             user = UserModel.objects.get(google_id=google_id)
             error = {"detail": ERROR_API['110'][1]}
             error_codes = [ERROR_API['110'][0]]
             return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)
        except UserModel.DoesNotExist:
            user = UserModel(email=email, last_name=last_name, first_name=first_name, google_id=google_id)
            user.is_active=True
            user.role = role
            if user.role == 'DOCTOR':
                user.is_active=False
                user.save()
                user.profile.doctor_license=doctor_license
                user.save()
            else:
                user.is_active=True
            user.save()
            user.profile.photo.save(name, content, save = True)
            user.save()
            first_login = True

    if user.google_id == google_id:
        if user.is_active != True:
            error = {"detail": ERROR_API['123'][1]}
            error_codes = [ERROR_API['123'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

        if user.role == 'CUSTOMER':
            if app == 'DOCTOR_APP':
                error = {"detail": ERROR_API['117'][1]}
                error_codes = [ERROR_API['117'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)
        if user.role == "DOCTOR":
            if app == 'CUSTOMER_APP':
                error = {"detail": ERROR_API['117'][1]}
                error_codes = [ERROR_API['117'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)

        token = create_login_token(user)
        profile = get_profile_data(user.id, request)
        content = {'token': token.key, 'email': user.email, 'id': user.id, 'first_login': first_login,
               'first_name': user.first_name, 'last_name': user.last_name, 'profile': profile,'doctor_license':user.profile.doctor_license}
        return Response(custom_api_response(content=content), status=status.HTTP_200_OK)
    else:
        error = {"detail": ERROR_API['120'][1]}
        error_codes = [ERROR_API['120'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)


from  account.utils import AREA_CHOICES,GENDER_CHOICES,SPECIALIZATION_CHOICES,NOTIFICATION_TYPES
from common.utils import LANGUAGES,ROLES
from simrequests.models import STATUSES,TYPES

@api_view(['GET'])
def ChoicesView(request):
    spec = {'specialization':SPECIALIZATION_CHOICES,
            'area':AREA_CHOICES,
            'notifications':NOTIFICATION_TYPES,
            'language':LANGUAGES,
            'role':ROLES,
            'status':STATUSES,
            'TYPES':TYPES}

    return Response(spec)


class UserResetPasswordRequestToken(ResetPasswordRequestToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # before we continue, delete all existing expired tokens
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # datetime.now minus expiry hours
        now_minus_expiry_time = timezone.now() - timedelta(hours=password_reset_token_validation_time)

        # delete all tokens where created_at < now - 24 hours
        ResetPasswordToken.objects.filter(created_at__lte=now_minus_expiry_time).delete()

        # find a user by email address (case insensitive search)
        users = User.objects.filter(email__iexact=email)

        active_user_found = False

        # iterate over all users and check if there is any user that is active
        # also check whether the password can be changed (is useable), as there could be users that are not allowed
        # to change their password (e.g., LDAP user)
        for user in users:
            if user.is_active and user.has_usable_password():
                active_user_found = True

        # No active user found, raise a validation error
        if not active_user_found:
            # raise ValidationError({
            #     'email': ValidationError(
            #         _("There is no active user associated with this e-mail address or the password can not be changed"),
            #         code='invalid')}
            # )
            error = {"detail": ERROR_API['104'][1]}
            error_codes = [ERROR_API['104'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)





        # last but not least: iterate over all users that are active and can change their password
        # and create a Reset Password Token and send a signal with the created token
        for user in users:
            if user.google_id != None:
                error = {"detail": ERROR_API['127'][1]}
                error_codes = [ERROR_API['127'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)
            if user.fb_id != None:
                error = {"detail": ERROR_API['126'][1]}
                error_codes = [ERROR_API['126'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)



            if user.is_active and user.has_usable_password():
                # define the token as none for now
                token = None

                # check if the user already has a token
                if user.password_reset_tokens.all().count() > 0:
                    # yes, already has a token, re-use this token
                    token = user.password_reset_tokens.all()[0]
                else:
                    # no token exists, generate a new token
                    token = ResetPasswordToken.objects.create(
                        user=user,
                        user_agent=request.META['HTTP_USER_AGENT'],
                        ip_address=request.META['REMOTE_ADDR']
                    )
                # send a signal that the password token was created
                # let whoever receives this signal handle sending the email for the password reset
                reset_password_token_created.send(sender=self.__class__, reset_password_token=token)

        return Response({'status': 'OK'},status=status.HTTP_200_OK)


class UserResetPasswordConfirm(ResetPasswordConfirm):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        token = serializer.validated_data['token']

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            # return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)
            error = {"detail": ERROR_API['113'][1]}
            error_codes = [ERROR_API['113'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            # return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)
            error = {"detail": ERROR_API['114'][1]}
            error_codes = [ERROR_API['114'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        # change users password
        if reset_password_token.user.has_usable_password():
            pre_password_reset.send(sender=self.__class__, user=reset_password_token.user)
            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(sender=self.__class__, user=reset_password_token.user)

        # Delete all password reset tokens for this user
        ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

        return Response({'status': 'OK'})



from django.views import View
from django.shortcuts import render
from common.forms import ChangePasswordForm
from django.http import HttpResponse


class NewPasswordConfirm(View):
    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm
        key = request.GET.get('key')
        if key != None:
            return render(template_name='new-password-form.html', request=self.request, context={'form': form,'key': key})
        return render(template_name='password-reset-error.html', request=self.request, context={'error':'No reset key.'})



    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():

            key = request.GET.get('key')

            password_reset_token_validation_time = get_password_reset_token_expiry_time()

            reset_password_token = ResetPasswordToken.objects.filter(key=key).first()

            if reset_password_token is None:
                return render(template_name='password-reset-error.html', request=request, context={'error': 'Reset key not provided. Please try change password again.'})


            expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

            if timezone.now() > expiry_date:
                # delete expired token
                reset_password_token.delete()
                # return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)
                return render('password-reset-error.html', request=request, context={'error': 'Reset key expired.'})

            password=form.cleaned_data['password1']

            if reset_password_token.user.fb_id != None:
                ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()
                return render(template_name='password-reset-error.html', request=request, context={'error': 'Account registered via Facebook. Please login via social network.'})

            if reset_password_token.user.google_id != None:
                ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()
                return render(template_name='password-reset-error.html', request=request, context={'error': 'Account registered via Google. Please login via social network.'})


            if reset_password_token.user.has_usable_password():
                pre_password_reset.send(sender=self.__class__, user=reset_password_token.user)
                reset_password_token.user.set_password(password)
                reset_password_token.user.save()
                post_password_reset.send(sender=self.__class__, user=reset_password_token.user)

                ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

                return render(template_name='password-reset-success.html', request=request)

        key = request.GET.get('key')

        if key == None:
            return render(template_name='password-reset-error.html',request=request,context={'error':'No reset key.'})

        return render(template_name='new-password-form.html', request=request, context={'form': form,
                                                                                        'key': key})


user_reset_password_confirm = UserResetPasswordConfirm.as_view()
user_reset_password_request_token = UserResetPasswordRequestToken.as_view()

@api_view(['GET'])
@permission_classes((AllowAny,))
def IsLoggedInView(request):
        if request.user.is_anonymous:
            error = {"detail": ERROR_API['119'][1]}
            error_codes = [ERROR_API['119'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated==True:
            error = {"detail": ERROR_API['200'][1]}
            error_codes = [ERROR_API['200'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_200_OK)
        else:
            error = {"detail": ERROR_API['119'][1]}
            error_codes = [ERROR_API['119'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

