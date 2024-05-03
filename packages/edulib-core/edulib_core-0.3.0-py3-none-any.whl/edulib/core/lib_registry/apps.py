# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)


class AppConfig(AppConfigBase):

    name = __package__

    def ready(self):
        self._register_repositories()

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )

        from .adapters.db import (
            exchange_fund,
            registry_entries,
        )

        bus.get_uow().register_repositories(
            ('exchange_fund', exchange_fund),
            ('registry_entries', registry_entries)
        )
