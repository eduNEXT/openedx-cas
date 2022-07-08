#!/usr/bin/env python
"""
Tests for the `openedx-cas` backends module.
"""
from django.conf import settings
from django.test import TestCase
import urllib.parse

from openedx_cas.backends import CASAuth


class TestOpenEdxCasAuthBackend(TestCase):
    """
    Test class to verify standard behavior of utility methods that belong to CASAuth.
    """

    def test_cas_serice_url_defined_in_settings(self):
        """
        This method is used to verify the CAS_SERVICE_URL variable in settings is updated after the call on CASAuth.auth_url

        Expected behavior:
        CASAuth.auth_url includes a query param called 'service' which value is a parsed string with the CAS_SERVICE_URL
        """
        # TODO: Use a Mock to replace CASAuth and the strategy param
        cas_backend = CASAuth(None)
        auth_url = cas_backend.auth_url()
        self.assertIn(urllib.parse.quote(settings.CAS_SERVICE_URL), auth_url)

    def test_auth_complete_ticket_validated(self):
        """
        This method is used to verify that the flow is valid when the ticket is valid

        Expected behavior:
        Response returned by auth_complete should include the correspoding values when the ticket is valid
        """
        ...

    def test_auth_complete_ticket_not_valid(self):
        """
        This method is used to verify that the flow is valid when the ticket is invalid

        Expected behavior:
        Response returned by auth_complete should include the correspoding values when the ticket is invalid
        """
        ...

    def test_get_user_details(self):
        """
        This method is used to verify that the user_details are returned correctly whenever those are or not in the
        response

        Expected behavior:
        Returns a dict with the corresponding information information
        """
        ...

    def test_get_user_id_exists(self):
        """
        This method is used to verify the username is returned when the details include it

        Expected behavior:
        Returns the username sended
        """
        ...

    def test_get_user_id_doesnt_exists(self):
        """
        This method is used to verify the method throws an error when the username is not defined

        Expected behavior:
        Throws an KeyError exception
        """
        ...
