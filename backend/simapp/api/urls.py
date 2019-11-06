from .common.user.urls import urlpatterns as user_urls
from .common.category.urls import urlpatterns as category_urls
from .account.urls import urlpatterns as account_urls
from .simmarket.company.urls import urlpatterns as company_urls
from .simmarket.simpackage.urls import urlpatterns as simpackage_urls
from .simpayments.urls import urlpatterns as payment_urls
from .simrequest.urls import urlpatterns as simrequest_urls
from .common.language.urls import urlpatterns as language_urls
from .simalert.urls import urlpatterns as alrts_urls
from .simSIPcalls.urls import urlpatterns as callSIP_urls
from .medical_history.urls import urlpatterns as medical_history_urls
from .simmarket.payments.urls import  urlpatterns as sim_card_payment_urls
from .common.push.urls import urlpatterns as push_notif_urls

urlpatterns = []
urlpatterns = urlpatterns + \
              user_urls + \
              account_urls + \
              category_urls + \
              company_urls + \
              simpackage_urls + \
              payment_urls + \
              simrequest_urls + \
              language_urls + \
              alrts_urls + \
              callSIP_urls + \
              medical_history_urls +\
              sim_card_payment_urls +\
              push_notif_urls


