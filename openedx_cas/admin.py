"""Admin classes for Open edX CAS."""
from django import forms
from django.contrib import admin

from openedx_cas.models import CAS_BACKENDS, CASProviderConfig

try:
    from config_models.admin import KeyedConfigurationModelAdmin
except ImportError:
    KeyedConfigurationModelAdmin = admin.ModelAdmin


class CASProviderConfigForm(forms.ModelForm):
    """Django Admin form class for CASProviderConfig."""

    backend_name = forms.ChoiceField(choices=((name, name) for name in CAS_BACKENDS))


class CASProviderConfigAdmin(KeyedConfigurationModelAdmin):
    """Django Admin class for CASProviderConfig."""

    form = CASProviderConfigForm


admin.site.register(CASProviderConfig, CASProviderConfigAdmin)
