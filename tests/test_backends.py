#!/usr/bin/env python
"""
Tests for the `openedx-cas` backends module.
"""
from unittest.mock import Mock, patch
from django.conf import settings
from django.test import TestCase
import urllib.parse
from ddt import data, ddt, unpack

from openedx_cas.backends import CASAuth


@ddt
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
        strategy = Mock()
        cas_backend = CASAuth(strategy=strategy)
        auth_url = cas_backend.auth_url()
        self.assertIn(urllib.parse.quote(settings.CAS_SERVICE_URL), auth_url)

    @patch('openedx_cas.backends.CASAuth.cas_validation')
    def test_auth_complete_ticket_validated(self):
        """
        This method is used to verify that the flow is valid when the ticket is valid

        Expected behavior:
        Response returned by auth_complete should include the correspoding values when the ticket is valid
        """
        strategy = Mock()
        cas_backend = CASAuth(strategy=strategy)
        service_response = {"ticket": "213123123-123123123"}
        request = Mock(GET=service_response)
        answer = cas_backend.auth_complete(request=request)
        # TODO In progress

    def test_auth_complete_ticket_not_valid(self):
        """
        This method is used to verify that the flow is valid when the ticket is invalid

        Expected behavior:
        Response returned by auth_complete should include the correspoding values when the ticket is invalid
        """
        ...

    @unpack
    @data({'username': 'test_has_value',
           'email': 'test_has_value',
           'fullname': 'test_has_value',
           'first_name': 'test_has_value',
           'last_name': 'test_has_value'},
          {'username': '',
           'first_name': '',
           'last_name': ''},
          {'username': ''},
          )
    def test_get_user_details(self, **kwargs):
        """
        This method is used to verify that the user_details are returned correctly whenever those are or not in the
        response

        Expected behavior:
        Returns a dict with the corresponding information
        """
        strategy = Mock()
        cas_backend = CASAuth(strategy=strategy)
        response = cas_backend.get_user_details(kwargs)

        for argument in kwargs:
            value = kwargs[argument]
            if value:
                self.assertEqual(value, response[argument])

    @unpack
    @data(
        (
            {'username': 'test_has_value'},
            {}
        ),
        (
            {'username': '123'},
            {}
        ),
        (
            {'username': 'abc'},
            {}
        ),
    )
    def test_get_user_id_exists(self, details, response):
        """
        This method is used to verify the username is returned when the details include it

        Expected behavior:
        Returns the username sended
        """
        strategy = Mock()
        cas_backend = CASAuth(strategy=strategy)

        username = cas_backend.get_user_id(details=details, response=response)
        self.assertEqual(username, details['username'])

    def test_get_user_id_doesnt_exists(self):
        """
        This method is used to verify the method throws an error when the username is not defined

        Expected behavior:
        Throws an KeyError exception
        """
        strategy = Mock()
        cas_backend = CASAuth(strategy=strategy)

        self.assertRaises(KeyError, lambda: cas_backend.get_user_id(details={}, response={}))
