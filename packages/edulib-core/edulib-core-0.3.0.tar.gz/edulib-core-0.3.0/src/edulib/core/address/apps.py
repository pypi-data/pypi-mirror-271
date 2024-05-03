# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from . import (
    domain,
)


class AppConfig(AppConfigBase):

    name = __package__

    def ready(self):
        self._register_repositories()
        self._register_handlers()

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )

        from .adapters.db import (
            repository,
        )

        bus.get_uow().register_repositories(('addresses', repository))

    def _register_handlers(self):
        from edulib.core import (
            bus,
        )

        from . import (
            services,
        )

        bus.add_command_handlers(
            (domain.CreateAddress, services.create_address),
            (domain.UpdateAddress, services.update_address),
            (domain.DeleteAddress, services.delete_address),
        )
