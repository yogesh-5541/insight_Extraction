"""
Providers package for langextract.

This module is responsible for loading and registering
built-in and plugin-based inference providers.
"""

# pylint: disable=invalid-name

from importlib import import_module
from typing import Dict, Type

from langextract.core.base import BaseLanguageModel

# Internal flags to avoid loading providers multiple times
_plugins_loaded = False
_builtins_loaded = False

# Registry for providers
PROVIDERS: Dict[str, Type[BaseLanguageModel]] = {}


def register_provider(name: str, provider_cls: Type[BaseLanguageModel]) -> None:
    """
    Register a language model provider.

    Args:
        name (str): Provider name
        provider_cls (Type[BaseLanguageModel]): Provider class
    """
    PROVIDERS[name] = provider_cls


def load_builtin_providers() -> None:
    """
    Load built-in providers shipped with langextract.
    """
    global _builtins_loaded

    if _builtins_loaded:
        return

    import_module("langextract.providers.openai")
    import_module("langextract.providers.huggingface")

    _builtins_loaded = True


def load_plugin_providers() -> None:
    """
    Load external plugin-based providers.
    """
    global _plugins_loaded

    if _plugins_loaded:
        return

    try:
        import_module("langextract_plugins")
    except ModuleNotFoundError:
        # Plugins are optional
        pass

    _plugins_loaded = True


def get_provider(name: str) -> Type[BaseLanguageModel]:
    """
    Retrieve a provider by name.

    Args:
        name (str): Provider name

    Returns:
        Type[BaseLanguageModel]: Provider class

    Raises:
        KeyError: If provider is not found
    """
    load_builtin_providers()
    load_plugin_providers()

    if name not in PROVIDERS:
        raise KeyError(f"Provider '{name}' not found")

    return PROVIDERS[name]
