from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
#from django.contrib import admin


def create_auth_token(sender, instance=None, created=False, **kwargs):
    # Действие, рассчитанное на сигнал после создания записи пользователя.
    # Таким образом создаем ему автоматически токен.
    # Для этого нужно подключить rest_framework.authtoken в INSTALLED_APPS.
    if created:
        Token.objects.create(user=instance)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender:
    :param reset_password_token:
    :param args:
    :param kwargs:
    :return:
    """
    current_site = Site.objects.get_current()
    change_password_token = reset_password_token.key

    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        # ToDo: The URL can (and should) be constructed using pythons built-in `reverse` method.
        'reset_password_url': "{protocol}://{domain}/api/v1/password-reset/confirm/?key={token}".format(token=change_password_token,
                                                                                  domain=current_site.domain,
                                                                                  protocol="http"),
        'site_name': current_site.name,
        'token': change_password_token
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        _("Password Reset for {title}".format(title=current_site.name)),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


