from django.conf.urls import re_path, include, url

from api.common.push.views import PushDeviceListCreate
urlpatterns = [
    url(r'^reg-device/$',PushDeviceListCreate.as_view(), name='reg_push_device'),

]