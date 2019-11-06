from django.conf.urls import re_path, include, url
from rest_framework import routers
from .views import UserViewSet, Logout, UserMe, UserIsExists, \
    user_reset_password_request_token, user_reset_password_confirm,\
    facebook_auth, google_auth, ChoicesView, IsLoggedInView
from . import views as api_view
from django.contrib.auth import views as auth_views

from django.urls import path


from .views import NewPasswordConfirm

router = routers.DefaultRouter()
router.include_format_suffixes = False
router.register(r'users', UserViewSet, base_name='UserView')

urlpatterns = router.urls

urlpatterns += [
    url(r'^registration/$', api_view.register_view, name='user_registration'),
    url(r'^login/$', api_view.login_view, name='user_login'),
    url(r'^logout/', Logout.as_view(), name='user_logout'),
    url(r'^user/me/', UserMe.as_view(), name='user_me'),
    url(r'^user/exists/', UserIsExists.as_view(), name='user_exists'),
    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^login-google/$', google_auth, name='google_login'),
    url(r'^login-facebook/$',facebook_auth , name='facebook_login'),


    url(r'^password-reset/$', user_reset_password_request_token, name='reset_password_request'),
    url(r'^password-reset/confirm/$', NewPasswordConfirm.as_view(), name='reset_password_confirm'),


    # url(r'^free-managers/', free_managers_view, name='free_managers'),
    # url(r'^login-twitter/', twitter_login),
    # url(r'^social-registration/', social_reg_view),
    # url(r'^social-unregistration/', social_unregister_view),
    url(r'^choices/$', ChoicesView),
    url(r'^login-check/$', IsLoggedInView),

]