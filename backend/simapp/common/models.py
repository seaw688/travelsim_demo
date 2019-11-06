from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db.models.signals import post_save
from . import receivers
from django.contrib.auth import get_user_model
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from . utils import ROLES, DEFAULT_USER_ROLE, LANGUAGES, DEFAULT_LANGUAGE



class CustomUserManager(UserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('username', 'admin')
        username = 'admin'

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, blank=True, unique=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    role = models.CharField(max_length=50, choices=ROLES, default=DEFAULT_USER_ROLE)
    creator_id = models.SmallIntegerField(default=0)
    fb_id = models.CharField(max_length=100, blank=True, unique=True, null=True)
    twitter_id = models.CharField(max_length=100, blank=True, unique=True, null=True)
    google_id = models.CharField(max_length=100, blank=True, unique=True, null=True)
    mobile = models.CharField(max_length=16,blank=True,null=True)
    language = models.CharField(max_length=100, choices=LANGUAGES, default=LANGUAGES[0][0])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    # objects = CustomUserManager()

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.get_full_name()

    class Meta:
        ordering = ['-id', ]


class Category(MPTTModel):
    category_name = models.CharField(max_length=64, unique=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='categories/%Y/%m/%d', blank=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['category_name']

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __unicode__(self):
        return self.category_name

    def __str__(self):
        return self.category_name


post_save.connect(receivers.create_auth_token, sender=get_user_model())


def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'language/{1}'.format(instance, filename)


class LanguageFile(models.Model):
        title = models.CharField(max_length=50,choices=LANGUAGES,unique=True)
        file = models.FileField(upload_to=file_directory_path)

PUSH_STATUSES = (('ACTIVE','active'),('DISABLED','disabled'))

class PushDevice(models.Model):
    player_id = models.UUIDField(null=True,blank=True)
    device_id = models.CharField(max_length=100,blank=True,null=True)
    status = models.CharField(choices=PUSH_STATUSES,default=PUSH_STATUSES[0][0],max_length=30)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

