from typing import ClassVar, Generic, TypeVar, cast

from mozilla_django_oidc.utils import import_from_settings

from .models import OpenIDConnectConfig, OpenIDConnectConfigBase

T = TypeVar("T", bound=OpenIDConnectConfigBase)


class SoloConfigMixin(Generic[T]):
    config_class: ClassVar[type[OpenIDConnectConfigBase]] = OpenIDConnectConfig
    _solo_config: T

    @property
    def config(self) -> T:
        if not hasattr(self, "_solo_config"):
            # django-solo and type checking is challenging, but a new release is on the
            # way and should fix that :fingers_crossed:
            config = self.config_class.get_solo()
            self._solo_config = cast(T, config)
        return self._solo_config

    def refresh_config(self) -> None:
        """
        Refreshes the cached config on the instance, required for middleware
        since middleware is only instantiated once (during the Django startup phase)
        """
        if hasattr(self, "_solo_config"):
            del self._solo_config

    def get_settings(self, attr, *args):
        attr_lowercase = attr.lower()
        if hasattr(self.config, attr_lowercase):
            # Workaround for OIDC_RP_IDP_SIGN_KEY being an empty string by default.
            # mozilla-django-oidc explicitly checks if `OIDC_RP_IDP_SIGN_KEY` is not `None`
            # https://github.com/mozilla/mozilla-django-oidc/blob/master/mozilla_django_oidc/auth.py#L189
            value_from_config = getattr(self.config, attr_lowercase)
            if value_from_config == "":
                return None
            return value_from_config
        return import_from_settings(attr, *args)


class GetAttributeMixin:
    def __getattribute__(self, attr: str):
        """
        Mixin used to avoid calls to the config model on __init__ and instead
        do these calls runtime
        """
        if not attr.startswith("OIDC"):
            return super().__getattribute__(attr)

        try:
            default = super().__getattribute__(attr)
        except AttributeError:
            default = None
        return self.get_settings(attr, default)
