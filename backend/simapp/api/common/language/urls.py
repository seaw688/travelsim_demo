from django.conf.urls import url
from .views import LanguageView,LanguageDetailView

urlpatterns = [
    url(r'^language/$', LanguageView.as_view()),
    url(r'^language/(?P<pk>[^/.]+)/$', LanguageDetailView.as_view()),

]