"""Centralized Authentication Service backend based on the social-core library
implementation.
"""
from social_core.backends.base import BaseAuth


class CASAuth(BaseAuth):
    """CAS authentication backend base class.

    Settings will be inspected to get more values names that should be
    stored on extra_data field. The setting name is created following the
    pattern SOCIAL_AUTH_<uppercase current backend name>_EXTRA_DATA.

    access_token is always stored.

    URLs settings:
        AUTHORIZATION_URL       Authorization service url
        ACCESS_TOKEN_URL        Access token URL
    """
    name = "centralized-auth-service"

    def auth_url(self):
        """Get the URL to which we must redirect in order to
        authenticate the user:

        Redirect /CAS-provider-domain/
        """
        raise NotImplementedError("Not implemented yet")

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance.

        We could use the implementation of:
        https://github.com/django-cas-ng/django-cas-ng/blob/master/django_cas_ng/backends.py#L22
        And refactor it as we see fit according our use case.

        Request:
        GET
	    https://CAS-provider-domain/auth/complete/?ticket=ticket
        """
        raise NotImplementedError("Not implemented yet")
