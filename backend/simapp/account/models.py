from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from simmarket.models import SimPackage
from django_encrypted_filefield.fields import EncryptedImageField
from . utils import GENDER_CHOICES, DEFAULT_USER_GENDER, NOTIFICATION_TYPES, AREA_CHOICES, SPECIALIZATION_CHOICES

User=get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    airline_image = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    travel_image = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    passport_image = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    medical_image = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)

    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default=DEFAULT_USER_GENDER)
    points = models.IntegerField(default=0, blank=True, null=True)
    rank = models.IntegerField(default=0, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True)
    subscribe = models.BooleanField(default=False)
    phone = models.CharField(max_length=16,blank=True,null=True)
    age = models.IntegerField(default=None, blank=True, null=True)
    notifications = models.CharField(max_length=100, choices=NOTIFICATION_TYPES,default=NOTIFICATION_TYPES[0][0])
    date_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    call_points = models.IntegerField(default=0)
    document_id = models.CharField(blank=True,null=True,max_length=100)
    doctor_license = models.IntegerField(blank=True,null=True)
    pbx_domain = models.CharField(max_length=100,blank=True,null=True)
    extension_number = models.CharField(max_length=100,blank=True,null=True)
    extension_password = models.CharField(max_length=100,blank=True,null=True)




    provider = models.CharField(max_length=200, blank=True, null=True)
    specialization = models.CharField(max_length=200, choices=SPECIALIZATION_CHOICES,blank=True, null=True)
    sim_number = models.CharField(max_length=16, blank=True, null=True)
    area = models.CharField(max_length=40,choices=AREA_CHOICES,blank=True,null=True)


    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



class UserSimPackage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_sim_package')
    created = models.DateTimeField(auto_now=True)
    package = models.ForeignKey(SimPackage,on_delete=models.CASCADE,related_name='package_users')
