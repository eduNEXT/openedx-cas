"""
Common settings for the Open edX Demo site.
"""


def plugin_settings(settings):
    """
    Defines openedx-demo-plugin settings when app is used as a plugin to edx-platform.
    See: https://github.com/openedx/edx-django-utils/tree/master/edx_django_utils/plugins
    """
    settings.CAS_SERVER_URL = "https://ingreso.preprod-ceibal.edu.uy/"
    settings.CAS_SERVER_LOGIN_URL = "https://ingreso.preprod-ceibal.edu.uy/loginunico/username.xhtml"
    if "openedx_cas.backends.CASAuth" not in settings.AUTHENTICATION_BACKENDS:
        settings.AUTHENTICATION_BACKENDS = ["openedx_cas.backends.CASAuth"] + settings.AUTHENTICATION_BACKENDS
    settings.CAS_CREATE_USER= True
    settings.CAS_VERSION = 3