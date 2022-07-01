"""Centralized Authentication Service backend based on the social-core library
implementation.
"""
from social_core.backends.base import BaseAuth
from social_core.exceptions import AuthFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django_cas_ng.backends import CASBackend
import urllib.parse
from django_cas_ng.utils import get_cas_client
from django.contrib.auth import get_user_model

import logging
import warnings

UserModel = get_user_model()

logger = logging.getLogger(__name__)

class CASBackendOverride(CASBackend):

    def cas_validation(self, request, ticket, service):
        client = get_cas_client(service_url=service, request=request)
        username, attributes, pgtiou = client.verify_ticket(ticket)

        if not username:
            message = f"Couldn't find username associated with ticket{ticket}"
            logger.error(message)
            raise AuthFailed(message)

        if attributes and request:
            request.session['attributes'] = attributes

        if settings.CAS_USERNAME_ATTRIBUTE != 'cas:user' and settings.CAS_VERSION != 'CAS_2_SAML_1_0':
            if attributes:
                username = attributes.get(settings.CAS_USERNAME_ATTRIBUTE)
            else:
                return None

        username = self.clean_username(username)

        if attributes:
            reject = self.bad_attributes_reject(request, username, attributes)
            if reject:
                logger.error(f"Attributes don't allowed {attributes}")
                return None

            # If we can, we rename the attributes as described in the settings file
            # Existing attributes will be overwritten
            for cas_attr_name, req_attr_name in settings.CAS_RENAME_ATTRIBUTES.items():
                if cas_attr_name in attributes and cas_attr_name is not req_attr_name:
                    attributes[req_attr_name] = attributes[cas_attr_name]
                    attributes.pop(cas_attr_name)

        if pgtiou and settings.CAS_PROXY_CALLBACK and request:
            request.session['pgtiou'] = pgtiou
        return {
            "username": username,
        }

class CASAuth(BaseAuth, CASBackendOverride):
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
        return f"{settings.CAS_SERVER_URL}?service={urllib.parse.quote(f'http://{settings.LMS_BASE}/auth/complete/centralized-auth-service/?next=/')}"

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
        request = kwargs['request']
        ticket = request.GET['ticket']
        service = f"http://{settings.LMS_BASE}/auth/complete/centralized-auth-service/?next=/"
        response = self.cas_validation(request, ticket, service)
        logger.info(f"CAS Response: {response}")
        kwargs.update({'response': response, 'backend': self})
        return self.strategy.authenticate(*args, **kwargs)

    def get_user_details(self, response):
        return {
            'username': response.get("username", ""),
            'email': response.get("email", ""),
            'fullname': response.get("fullname", ""),
            'first_name': response.get("first_name", ""),
            'last_name': response.get("last_name", ""),
        }

    def get_user_id(self, details, response):
        return details['username']
