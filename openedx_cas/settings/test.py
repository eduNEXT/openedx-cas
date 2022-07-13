"""
Common test settings for the Open edX Demo site.
"""
from .common import *


class SettingsClass:
    """ dummy settings class """


def plugin_settings(settings):
    """
    Defines openedx-demo-plugin settings when app is used as a plugin to edx-platform.
    See: https://github.com/openedx/edx-django-utils/tree/master/edx_django_utils/plugins
    """


SETTINGS = SettingsClass()
plugin_settings(SETTINGS)
vars().update(SETTINGS.__dict__)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'default.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SECRET_KEY = 'insecure-secret-key'

LMS_BASE = 'https://local.overhangio.io'
CAS_SERVER_URL = 'https://local.overhangio.io'
CAS_SERVICE_URL = 'https://local.overhangio.io'

CAS_CREATE_USER = False
CAS_VERSION = 3
CAS_VERIFY_SSL_CERTIFICATE = False
CAS_EXTRA_LOGIN_PARAMS = None
CAS_RENEW = False
CAS_USERNAME_ATTRIBUTE = "cas:user"
CAS_PROXY_CALLBACK = None
CAS_SESSION_FACTORY = None
CAS_RENAME_ATTRIBUTES = {}
