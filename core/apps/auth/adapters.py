
from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailConfirmation
from allauth.utils import build_absolute_uri
from anymail.exceptions import (
    AnymailError,
    AnymailRequestsAPIError,
)
from sentry_sdk import capture_exception
from templated_email import send_templated_mail

from core.apps.emails.utils import get_default_email_context


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def get_email_confirmation_url(
            self,
            request: HttpRequest,
            emailconfirmation: EmailConfirmation,
    ):
        # link to frontend url for future redirection
        url = f'/auth/confirm-email/{emailconfirmation.key}/'
        return build_absolute_uri(request, url)

    def send_confirmation_mail(
            self,
            request: HttpRequest,
            emailconfirmation: EmailConfirmation,
            *args, **kwargs,
    ):
        text_message = "There is a problem sending mail at this moment!" \
                       "Please check your email or try again later."
        try:
            activate_url = self.get_email_confirmation_url(request, emailconfirmation)
            email_address = emailconfirmation.email_address
            context = get_default_email_context()
            context.update(
                name=email_address.user.name,
                verified_link=activate_url,
                site_name='EventsApp',  # FIXME
            )

            send_templated_mail(
                template_name='email_confirmation.email',
                recipient_list=[email_address],
                from_email=settings.TEMPLATED_EMAIL_FROM_EMAIL,
                context=context,
            )
        except (AnymailRequestsAPIError, AnymailError, Exception) as anymail_error:
            capture_exception(anymail_error)
            raise ValidationError(_(text_message)) from anymail_error
