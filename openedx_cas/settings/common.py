"""
Common settings for the Open edX Demo site.
"""


def plugin_settings(settings):
    """
    Defines openedx-demo-plugin settings when app is used as a plugin to edx-platform.
    See: https://github.com/openedx/edx-django-utils/tree/master/edx_django_utils/plugins
    """

    if "openedx_cas.backends.CASAuth" not in settings.AUTHENTICATION_BACKENDS:
        settings.AUTHENTICATION_BACKENDS = ["openedx_cas.backends.CASAuth"] + settings.AUTHENTICATION_BACKENDS
    settings.CAS_CREATE_USER = False
    settings.CAS_VERSION = 3
    settings.CAS_VERIFY_SSL_CERTIFICATE = False
    settings.CAS_EXTRA_LOGIN_PARAMS = None
    settings.CAS_RENEW = False
    settings.CAS_USERNAME_ATTRIBUTE = "cas:user"
    settings.CAS_PROXY_CALLBACK = None
    settings.CAS_SESSION_FACTORY = None
    settings.CAS_RENAME_ATTRIBUTES = {}
