"""
openedx_cas Django application initialization.
"""

from django.apps import AppConfig


class OpenedxCasConfig(AppConfig):
    """
    Configuration for the openedx_cas Django application.
    """

    name = 'openedx_cas'
    verbose_name = 'Centralized Authentication Service (CAS)'

    plugin_app = {
        'settings_config': {
            'lms.djangoapp': {
                'test': {'relative_path': 'settings.test'},
                'common': {'relative_path': 'settings.common'}
            }
        },
    }

    def ready(self):
        """Execute functions once the plugin finished loading."""
        from openedx_cas.proxy import load_registry_override  # pylint: disable=import-outside-toplevel
        load_registry_override()
