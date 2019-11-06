from django.conf.urls import url
from .views import ProfileDetailView, ProfilePhotoView, MyFetchView
from django_encrypted_filefield.constants import FETCH_URL_NAME

urlpatterns = [
    url(r'^user/profile/$', ProfileDetailView.as_view(), name='user_profile'),
    url(r'^user/profile/photo/$', ProfilePhotoView.as_view(), name='user_profile_photo'),
    url(r'^user/profile/(?P<user_id>\d+)/$', ProfileDetailView.as_view(), name='user_profile_detail'),
    url(r'^my-fetch-url/(?P<path>.+)',MyFetchView.as_view(),  name=FETCH_URL_NAME),
]