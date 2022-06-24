"""Centralized Authentication Service backend based on the social-core library
implementation.
"""
from social_core.backends.base import BaseAuth
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django_cas_ng.backends import CASBackend
import urllib.parse

import warnings

class CASAuth(CASBackend, BaseAuth):
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
        return f"{settings.CAS_SERVER_URL}?service={urllib.parse.quote(f'http://{settings.LMS_BASE}/auth/complete/centralized-auth-service/?next=/login')}"

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance.

        We could use the implementation of:
        https://github.com/django-cas-ng/django-cas-ng/blob/master/django_cas_ng/backends.py#L22
        And refactor it as we see fit according our use case.

        Request:
        GET
	    https://CAS-provider-domain/auth/complete/?ticket=ticket
        :returns: [User] Authenticated User object or None if authenticate failed
        """
        """
        Verifies CAS ticket and gets or creates User object
        
        """
        request = kwargs['request']
        ticket = request.GET['ticket']
        service = f"http://{settings.LMS_BASE}/auth/complete/centralized-auth-service/?next=/login"

        x = super(CASAuth, self).authenticate(request=request, ticket=ticket, service=service)
        
        kwargs.update({'backend':self})

        return self.strategy.authenticate(*args, **kwargs)