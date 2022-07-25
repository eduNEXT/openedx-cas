#!/usr/bin/env python
"""
Tests for the `openedx-cas` backends module.
"""
import urllib.parse
from unittest.mock import Mock, patch

from ddt import data, ddt, unpack
from django.conf import settings
from django.test import TestCase, override_settings
from social_core.exceptions import AuthFailed, AuthMissingParameter

from openedx_cas.backends import CASAuth


@ddt
class TestOpenEdxCasAuthBackend(TestCase):
    """
    Test class to verify standard behavior of utility methods that belong to CASAuth.
    """

    def setUp(self) -> None:
        super().setUp()
        strategy = Mock()
        self.cas_backend = CASAuth(strategy=strategy)

    def test_cas_service_url_defined_in_settings(self):
        """
        This method is used to verify the CAS_SERVICE_URL variable in settings is contained
        into the auth_url as a query parameter called service.

        Expected behavior:
        CASAuth.auth_url includes a query param called 'service' which value is a parsed
        string with the CAS_SERVICE_URL
        """
        auth_url = self.cas_backend.auth_url()

        self.assertIn(urllib.parse.quote(settings.CAS_SERVICE_URL), auth_url)

    @override_settings(CAS_SERVER_URL=None)
    def test_cas_server_url_undefined_in_settings(self):
        """
        This method is used to verify that when the variable CAS_SERVER_URL is undefined
        and proper error is raised.

        Expected behavior:
        raise AuthMissingParameter
        """
        self.assertRaises(AuthMissingParameter, self.cas_backend.auth_url)

    @override_settings(CAS_SERVICE_URL=None)
    def test_cas_service_url_undefined_in_settings(self):
        """
        This method is used to verify that when the variable CAS_SERVICE_URL is undefined
        and proper error is raised.

        Expected behavior:
        raise AuthMissingParameter
        """
        self.assertRaises(AuthMissingParameter, self.cas_backend.auth_url)

    @patch('openedx_cas.backends.CASAuth.cas_validation')
    def test_auth_complete_ticket_validated(self, cas_validation):
        """
        This method is used to verify that the flow is valid when the ticket is valid.

        Expected behavior:
        Response returned by auth_complete should include the correspoding values when the ticket is valid
        """
        cas_validation.return_value = {'username': 'edxplatform'}
        service_response = {"ticket": "213123123-123123123"}
        request = Mock(GET=service_response)

        self.cas_backend.auth_complete(request=request)

        self.cas_backend.strategy.authenticate.assert_called_with(
            request=request,
            response={'username': 'edxplatform'},
            backend=self.cas_backend
        )

    @unpack
    @data(
        {
            'username': 'test_has_value',
            'email': 'test_has_value',
            'fullname': 'test_has_value',
            'first_name': 'test_has_value',
            'last_name': 'test_has_value'
        },
        {
            'username': '',
            'first_name': '',
            'last_name': ''
        },
        {
            'username': ''
        },
    )
    def test_get_user_details(self, **kwargs):
        """
        This method is used to verify that the user_details are returned correctly whenever those are or not in the
        response

        Expected behavior:
        Returns a dict with the corresponding information
        """
        response = self.cas_backend.get_user_details(kwargs)

        for key, value in kwargs.items():
            if value:
                self.assertEqual(value, response[key])

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
        username = self.cas_backend.get_user_id(details=details, response=response)

        self.assertEqual(username, details['username'])

    def test_get_user_id_doesnt_exists(self):
        """
        This method is used to verify the method throws an error when the username is not defined

        Expected behavior:
        Throws an KeyError exception
        """
        self.assertRaises(KeyError, self.cas_backend.get_user_id, details={}, response={})

    @patch('openedx_cas.backends.get_cas_client')
    @data(
        ('edxplatform', [], None)
    )
    @unpack
    def test_cas_validation_returns_username(self, username, attributes, pgtiou, get_cas_client):
        """
        This method is used to verify the cas_validation method returns none when there is no username found.
        If the username is not found that's because the user is not registered in the platform.

        Expected behavior:
        Returns none
        """
        get_cas_client.return_value.verify_ticket.return_value = (username, attributes, pgtiou)
        request = Mock()
        ticket = 'dummy-ticket'
        service = 'dummy.service'

        response = self.cas_backend.cas_validation(request, ticket, service)

        self.assertDictEqual({"username": username}, response)

    @patch('openedx_cas.backends.get_cas_client')
    def test_cas_validation_returns_none_when_no_username(self, get_cas_client):
        """
        This method is used to verify the cas_validation method returns the username whenever it's found.

        Expected behavior:
        Returns a dict with a key called 'username'
        """
        get_cas_client.return_value.verify_ticket.return_value = (None, None, None)
        request = Mock()
        ticket = 'dummy-ticket'
        service = 'dummy.service'

        self.assertRaises(AuthFailed, self.cas_backend.cas_validation, request, ticket, service)
