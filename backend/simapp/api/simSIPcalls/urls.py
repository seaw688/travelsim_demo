from django.conf.urls import url
from .views import CallInitiationCallback, CallStartedCallback, CallEndedCallback, CallHistoryView, CurrentCallUserInfo, ListVoipCallsPack, CallbackCheck

urlpatterns = [
    url(r'^call-request/$', CallInitiationCallback),
    url(r'^call-started/$', CallStartedCallback),
    url(r'^call-ended/$', CallEndedCallback),

    url(r'^call-history/$', CallHistoryView.as_view()),
    url(r'^call-user/$', CurrentCallUserInfo.as_view()),

    url(r'^call-pack-list/$', ListVoipCallsPack.as_view()),

    url(r'^call-test/$', CallbackCheck),

]