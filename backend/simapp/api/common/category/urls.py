from django.conf.urls import re_path, include, url
from .views import CategoryList
from . import views as api_view


urlpatterns = [
    url(r'^categories/$', CategoryList.as_view()),
]