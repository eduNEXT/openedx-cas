"""Database models for Open edX CAS integration."""
from django.conf import settings
from django.contrib.sites.models import Site

try:
    from common.djangoapps.third_party_auth.models import (
        _LTI_BACKENDS,
        _PSA_OAUTH2_BACKENDS,
        _PSA_SAML_BACKENDS,
        LTIProviderConfig,
        OAuth2ProviderConfig,
        ProviderConfig,
        SAMLConfiguration,
        SAMLProviderConfig,
    )
    from common.djangoapps.third_party_auth.provider import Registry
    from openedx.core.djangoapps.theming.helpers import get_current_request
except ImportError:
    _LTI_BACKENDS = []
    _PSA_OAUTH2_BACKENDS = []
    _PSA_SAML_BACKENDS = []
    LTIProviderConfig = object
    OAuth2ProviderConfig = object
    SAMLConfiguration = object
    SAMLProviderConfig = object
    ProviderConfig = object

CAS_BACKENDS = ["centralized-auth-service"]


class CASProviderConfig(ProviderConfig):
    """General configuration required for this Open edX instance to act as CAS Service Provider."""

    KEY_FIELDS = ("slug",)
    prefix = "cas"
    backend_name = "centralized-auth-service"

    class Meta:
        """Meta class for CASProviderConfig."""

        app_label = "openedx_cas"
        verbose_name = "Provider Configuration (CAS)"
        verbose_name_plural = verbose_name

    def get_setting(self, name):
        """Get the value of a CAS setting from the Django Settings object.

        Raises:
            AttributeError when name is not configured.
        """
        return getattr(settings, f"CAS_{name.upper()}")


class RegistryOverride(Registry):
    """Class override for TPA Registry API specifically adding CAS providers."""

    @classmethod
    def _enabled_providers(cls):
        """Return all enabled providers for the current site.

        Arguments:
            cls: current registry class.

        Yields:
            Instances of ProviderConfig.
        """
        oauth2_backend_names = OAuth2ProviderConfig.key_values("backend_name", flat=True)
        for oauth2_backend_name in oauth2_backend_names:
            provider = OAuth2ProviderConfig.current(oauth2_backend_name)
            if provider.enabled_for_current_site and provider.backend_name in _PSA_OAUTH2_BACKENDS:
                yield provider
        if SAMLConfiguration.is_enabled(Site.objects.get_current(get_current_request()), "default"):
            idp_slugs = SAMLProviderConfig.key_values("slug", flat=True)
            for idp_slug in idp_slugs:
                provider = SAMLProviderConfig.current(idp_slug)
                if provider.enabled_for_current_site and provider.backend_name in _PSA_SAML_BACKENDS:
                    yield provider
        for consumer_key in LTIProviderConfig.key_values("lti_consumer_key", flat=True):
            provider = LTIProviderConfig.current(consumer_key)
            if provider.enabled_for_current_site and provider.backend_name in _LTI_BACKENDS:
                yield provider
        for provider_key in CASProviderConfig.key_values("slug", flat=True):
            provider = CASProviderConfig.current(provider_key)
            if provider.enabled_for_current_site:
                yield provider

    @classmethod
    def get_from_pipeline(cls, running_pipeline):  # pylint: disable=inconsistent-return-statements
        """Get the provider that is being used for the specified pipeline (or None).

        Arguments:
            running_pipeline: The python-social-auth pipeline being used to
                authenticate a user.

        Returns:
            An instance of ProviderConfig or None.
        """
        for enabled in cls._enabled_providers():
            if enabled.is_active_for_pipeline(running_pipeline):
                return enabled

    @classmethod
    def get_enabled_by_backend_name(cls, backend_name):
        """Return all enabled providers for the current site.

        Example:
            >>> list(get_enabled_by_backend_name("tpa-saml"))
                [<SAMLProviderConfig>, <SAMLProviderConfig>]

        Arguments:
            backend_name: The name of a python-social-auth backend used by
                one or more providers.

        Yields:
            Instances of ProviderConfig.
        """
        if backend_name in _PSA_OAUTH2_BACKENDS:
            oauth2_backend_names = OAuth2ProviderConfig.key_values("backend_name", flat=True)
            for oauth2_backend_name in oauth2_backend_names:
                provider = OAuth2ProviderConfig.current(oauth2_backend_name)
                if provider.backend_name == backend_name and provider.enabled_for_current_site:
                    yield provider
        elif backend_name in _PSA_SAML_BACKENDS and SAMLConfiguration.is_enabled(
                Site.objects.get_current(get_current_request()), "default"):
            idp_names = SAMLProviderConfig.key_values("slug", flat=True)
            for idp_name in idp_names:
                provider = SAMLProviderConfig.current(idp_name)
                if provider.backend_name == backend_name and provider.enabled_for_current_site:
                    yield provider
        elif backend_name in _LTI_BACKENDS:
            for consumer_key in LTIProviderConfig.key_values("lti_consumer_key", flat=True):
                provider = LTIProviderConfig.current(consumer_key)
                if provider.backend_name == backend_name and provider.enabled_for_current_site:
                    yield provider
        elif backend_name in CAS_BACKENDS:
            for provider_key in CASProviderConfig.key_values("slug", flat=True):
                provider = CASProviderConfig.current(provider_key)
                if provider.enabled_for_current_site:
                    yield provider
