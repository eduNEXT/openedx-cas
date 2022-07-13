"""Where helper methods for monkey patching strategy are implemented.

These proxies are created so we override classes inside the Open edX core without
the maintainability costs.
"""
from importlib import import_module

from openedx_cas.models import RegistryOverride


def load_registry_override():
    """Load registry class override when plugin is ready."""
    modules = ["common.djangoapps.third_party_auth.provider", "openedx.features.enterprise_support.api"]
    set_as_proxy(modules, "Registry", RegistryOverride)


def set_as_proxy(modules, model, proxy):
    """Patch a loaded module with a proxy object that has all the override registry properties.

    Arguments:
        modules: modules where the to override are implemented.
        model: class or model to replace.
        proxy: class or model that works as the replacement.
    """
    if isinstance(modules, str):
        modules = set([modules])

    for module in modules:
        module = import_module(module)
        setattr(module, model, proxy)
