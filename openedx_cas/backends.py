"""
Centralized Authentication Service backend based on the social-core library implementation.

Implements two backends, CASBackendOverride that allows us to perform the changes to the cas_validation
method, making it compatible with the BaseAuth class.
"""
import logging
import urllib.parse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django_cas_ng.backends import CASBackend
from django_cas_ng.utils import get_cas_client
from social_core.backends.base import BaseAuth
from social_core.exceptions import AuthFailed, AuthMissingParameter

UserModel = get_user_model()

logger = logging.getLogger(__name__)


class CASAuth(BaseAuth, CASBackend):
    """
    CAS authentication backend base class.

    Settings will be inspected to get more values names that should be
    stored on extra_data field. The setting name is created following the
    pattern SOCIAL_AUTH_<uppercase current backend name>_EXTRA_DATA.

    URLs settings:
        CAS_SERVICE_URL:
            Our authorization service url.
        CAS_CLIENT_VERSION:
            Version of client protocol.
            Currently V2 and V3 versions are supported, not sure how V1 will perform
        CAS_SERVER_URL:
            Server URL against the user is authenticated
    """

    name = "centralized-auth-service"

    def auth_url(self):
        """
        Get the URL to which we must redirect in order to authenticate the user.

        Redirect /CAS-service-domain/
        """
        if not getattr(settings, "CAS_SERVER_URL", None):
            raise AuthMissingParameter(self, "CAS_SERVER_URL")
        if not getattr(settings, "CAS_SERVICE_URL", None):
            raise AuthMissingParameter(self, "CAS_SERVICE_URL")
        return f"{settings.CAS_SERVER_URL}?service={urllib.parse.quote(settings.CAS_SERVICE_URL)}"

    def auth_complete(self, *args, **kwargs):
        """
        Completes login process, must return user instance.

        Request:
        GET https://CAS-service-domain/auth/complete/?ticket=ticket
        :returns: [User] Authenticated User object or None if authenticate failed
        """
        request = kwargs["request"]
        ticket = request.GET.get("ticket", None)

        if not ticket:
            logger.error("Ticket was not found in the request to authenticate user")
            # The setting is added to allow changing the behavior when there is not
            # ticket in the request. Usually when the user changes his password.
            if getattr(settings, "CAS_REDIRECT_WITHOUT_TICKET", None):
                return redirect(settings.LOGIN_URL)
            else:
                raise AuthMissingParameter(self, "ticket")

        response = self.cas_validation(request, ticket, settings.CAS_SERVICE_URL)
        kwargs.update({"response": response, "backend": self})

        logger.info(f"User {response} logged in with {settings.CAS_SERVER_URL}")

        return self.strategy.authenticate(*args, **kwargs)

    def cas_validation(self, request, ticket, service):
        """
        Perform the CAS ticket validation process.

        Overrides CASBackend.cas_validation to make it compatible with third_party_auth app.

        Get the CAS_CLIENT based on the settings.CAS_VERSION and verify the ticket
        which returns the authentication information of the user.

        Arguments:
            request: HttpRequest.
            ticket:  str containing the ticket key.
            service: str containing the service URL which is used to return.
        Returns:
            - A dictionary containing the username when the validation flow succeeds
            - None when the username attribute is changed
        Raise:
            - AuthFailed exception the username attribute is not found
        """
        client = get_cas_client(service_url=service, request=request)
        username, attributes, pgtiou = client.verify_ticket(ticket)  # pylint: disable=no-member

        if not username:
            message = "Couldn't find username by ticket"
            logger.error(message)
            raise AuthFailed(message)

        if attributes and request:
            request.session["attributes"] = attributes

        if settings.CAS_USERNAME_ATTRIBUTE != "cas:user" and settings.CAS_VERSION != "CAS_2_SAML_1_0":
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
            request.session["pgtiou"] = pgtiou

        return {
            "username": username,
        }

    def get_user_details(self, response):
        """Return user details from service provider response."""
        return {
            "username": response.get("username", ""),
            "email": response.get("email", ""),
            "fullname": response.get("fullname", ""),
            "first_name": response.get("first_name", ""),
            "last_name": response.get("last_name", ""),
        }

    def get_user_id(self, details, response):
        """Override to identify user by username."""
        return details["username"]

    def auth_html(self):
        """Empty override to avoid abstract quality errors."""
