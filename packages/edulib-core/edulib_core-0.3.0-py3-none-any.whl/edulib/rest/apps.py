from django.apps import (
    AppConfig as BaseAppConfig,
)


class AppConfig(BaseAppConfig):
    """Конфигурация приложения."""

    name = __package__
