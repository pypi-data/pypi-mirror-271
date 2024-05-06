import types
from functools import wraps
from typing import Annotated, Any, get_origin

from django.apps import AppConfig
from django.conf import settings
from django.core.cache import BaseCache, caches
from django.db import connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.urls import get_resolver
from django.utils.module_loading import import_string

import anydi

from ._utils import iter_urlpatterns


class ContainerConfig(AppConfig):  # type: ignore[misc]
    name = "anydi.ext.django"
    label = "anydi_django"

    # Prefix for Django settings
    settings_prefix = "django.conf.settings"

    def __init__(self, app_name: str, app_module: types.ModuleType | None) -> None:
        super().__init__(app_name, app_module)
        # Create a container
        self.container = anydi.Container(
            strict=getattr(settings, "ANYDI_STRICT_MODE", False),
        )

    def ready(self) -> None:
        # Register Django settings
        if getattr(settings, "ANYDI_REGISTER_SETTINGS", False):
            self.register_settings()

        # Register Django components
        if getattr(settings, "ANYDI_REGISTER_COMPONENTS", False):
            self.register_components()

        # Register modules
        for module_path in getattr(settings, "ANYDI_MODULES", []):
            module_cls = import_string(module_path)
            self.container.register_module(module_cls)

        # Patching the django-ninja framework if it installed
        if getattr(settings, "ANYDI_PATCH_NINJA", False):
            self.patch_ninja()

        # Auto-injecting the container into views
        if urlconf := getattr(settings, "ANYDI_AUTO_INJECT_URLCONF", None):
            self.auto_inject_urlconf(urlconf)

    def register_settings(self) -> None:  # noqa: C901
        """Register Django settings into the container."""

        def _get_setting_value(value: Any) -> Any:
            return lambda: value

        for setting_name, value in settings.__dict__.items():
            if not setting_name.isupper():
                continue
            self.container.register(
                Annotated[Any, f"{self.settings_prefix}.{setting_name}"],
                _get_setting_value(value),
                scope="singleton",
            )

        def _aware_settings(interface: Any) -> Any:
            origin = get_origin(interface)
            if origin is not Annotated:
                return interface
            named = interface.__metadata__[-1]

            if isinstance(named, str):
                _, setting_name = named.rsplit(self.settings_prefix, maxsplit=1)
                return Annotated[Any, f"{self.settings_prefix}.{setting_name}"]
            return interface

        def _resolve(resolve: Any) -> Any:
            @wraps(resolve)
            def wrapper(interface: Any) -> Any:
                return resolve(_aware_settings(interface))

            return wrapper

        def _aresolve(resolve: Any) -> Any:
            @wraps(resolve)
            async def wrapper(interface: Any) -> Any:
                return await resolve(_aware_settings(interface))

            return wrapper

        # Patch resolvers
        self.container.resolve = _resolve(self.container.resolve)  # type: ignore[method-assign]  # noqa
        self.container.aresolve = _aresolve(self.container.aresolve)  # type: ignore[method-assign]  # noqa

    def register_components(self) -> None:
        """Register Django components into the container."""

        # Register caches
        def _get_cache(cache_name: str) -> Any:
            return lambda: caches[cache_name]

        for cache_name in caches:
            self.container.register(
                Annotated[BaseCache, cache_name],
                _get_cache(cache_name),
                scope="singleton",
            )

        # Register database connections

        def _get_connection(alias: str) -> Any:
            return lambda: connections[alias]

        for alias in connections:
            self.container.register(
                Annotated[BaseDatabaseWrapper, alias],
                _get_connection(alias),
                scope="singleton",
            )

    def auto_inject_urlconf(self, urlconf: str) -> None:
        """Auto-inject the container into views."""
        resolver = get_resolver(urlconf)
        for pattern in iter_urlpatterns(resolver.url_patterns):
            # Skip django-ninja views
            if pattern.lookup_str.startswith("ninja."):
                continue
            pattern.callback = self.container.inject(pattern.callback)

    @staticmethod
    def patch_ninja() -> None:
        """Patch the django-ninja framework."""
        from .ninja import patch

        patch()
