# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)


class AppConfig(AppConfigBase):

    name = __package__

    def ready(self):
        self._register_commands()
        self.register_repositories()

    def _register_commands(self):
        from edulib.core import (
            bus,
        )

        from . import (
            domain,
            services,
        )

        bus.add_command_handlers(
            (domain.DeliverExamples, services.deliver_examples),
        )

    def register_repositories(self):
        from edulib.core import (
            bus,
        )

        from .adapters.db import (
            issuance_deliveries,
        )

        bus.get_uow().register_repositories(('issuance_deliveries', issuance_deliveries))
