"""
openedx_cas Django application initialization.
"""

from django.apps import AppConfig


class OpenedxCasConfig(AppConfig):
    """
    Configuration for the openedx_cas Django application.
    """

    name = 'openedx_cas'

    plugin_app = {
        'settings_config': {
            'lms.djangoapp': {
                'test': {'relative_path': 'settings.test'},
                'common': {'relative_path': 'settings.common'}
            }
        },
    }