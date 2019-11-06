from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import validate_password as vp
from django.contrib.auth import get_user_model
from rest_framework import serializers
#from rest_framework.compat import authenticate
from rest_framework.authentication import authenticate

from common.utils import ROLES, DEFAULT_USER_ROLE, LANGUAGES
from account.models import Profile
from ...utils import ERROR_API
#from ...common.category.serializers import CategorySerializer

UserModel = get_user_model()

APP = ('DOCTOR_APP', 'CUSTOMER_APP')


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(allow_blank=False, write_only=True)
    role = serializers.CharField(allow_blank=True, default=DEFAULT_USER_ROLE)
    creator_id = serializers.IntegerField(allow_null=True, write_only=True, required=False)
    username = serializers.CharField(allow_blank=True, required=False)
    profile = serializers.SerializerMethodField()
    # def validate(self, attrs):
    #     if attrs['password'] != attrs.pop('confirm_password'):
    #         raise serializers.ValidationError({'confirm_password':
    #                                                _('Passwords do not match')})
    #     return attrs

    def validate_password(self, value):
        vp(value)

        return value

    def validate_username(self, value):
        if value == '':
            return None

        # method = self.context['request'].method
        try:
            pk = int(self.context['request'].parser_context['kwargs']['pk'])
        except:
            pk = None

        try:
            user = UserModel.objects.get(username=value)
        except UserModel.DoesNotExist:
            user = None

        if user and user.username != '':
            if user.pk != pk:
                msg = _(ERROR_API['102'][1])
                api_error_code = ERROR_API['102'][0]
                raise serializers.ValidationError(msg, code=api_error_code)
            else:
                return value
        else:
            return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        #Profile.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.language = validated_data.get('language', instance.language)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        password = validated_data.get('password')
        if password:
            instance.set_password(validated_data.get('password'))
        instance.save()

        return instance

    def get_profile(self,obj):
        from api.account.serializers import ProfileSerializerUpdate
        from account.models import Profile
        try:
            profile = Profile.objects.get(user=obj)
            ser = ProfileSerializerUpdate(instance=profile)
            return ser.data

        except Profile.DoesNotExist:
            return None


    class Meta:
        model = UserModel
        fields = ('id', 'password', 'username', 'first_name', 'last_name', 'email', 'role',
                  'creator_id', 'language','date_joined', 'is_active', 'profile')
        write_only_fields = ('password', )



class RegisterUserSerializer(CustomUserSerializer):
    date_birth = serializers.DateField(allow_null=True, required=False)
    phone = serializers.CharField(allow_null=True, required=False)
    subscribe = serializers.NullBooleanField(required=False)
    license_number = serializers.IntegerField(allow_null=True,required=False)
    class Meta:
        model = UserModel
        fields = ('id', 'password', 'username', 'first_name', 'last_name', 'email', 'role', 'creator_id',
                  'date_birth', 'phone', 'subscribe','license_number')
        write_only_fields = ('password', )

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    app = serializers.CharField(allow_blank=True, required=False, default=APP[1])
    role = serializers.CharField(allow_blank=True, required=False, default=DEFAULT_USER_ROLE)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        app = attrs.get('app')
        role = attrs.get('role')

        temp_user = UserModel.objects.filter(email=email).first()


        if temp_user != None:

            if temp_user.is_active == False:
                msg = _(ERROR_API['123'][1])
                api_error_code = ERROR_API['123'][0]
                raise serializers.ValidationError(msg, code=api_error_code)



        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _(ERROR_API['101'][1])
                api_error_code = ERROR_API['101'][0]
                #raise serializers.ValidationError(msg, code='authorization')
                raise serializers.ValidationError(msg, code=api_error_code)

        else:
            # msg = _('Must include "email" and "password".')
            msg = _(ERROR_API['105'][1])
            api_error_code = ERROR_API['105'][0]
            raise serializers.ValidationError(msg, code=api_error_code)

        attrs['user'] = user
        return attrs


class UserIsExistsSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))

    def validate(self, attrs):
        email = attrs.get('email')

        if email:
            user = UserModel.objects.filter(email=email).all()

            if not user:
                # msg = _('User does not exists')
                msg = _(ERROR_API['104'][1])
                api_error_code = ERROR_API['104'][0]
                raise serializers.ValidationError(msg, code=api_error_code)
        else:
            # msg = _('Must include "email".')
            msg = _(ERROR_API['106'][1])
            api_error_code = ERROR_API['106'][0]
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs



class SocialRegistrationSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=('GOOGLE','FACEBOOK'),required=True)
    social_token = serializers.CharField(max_length=10000)


class SocialAuthSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=10000)

