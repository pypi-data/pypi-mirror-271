# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from edulib.core.directory import (
    domain,
)


class AppConfig(AppConfigBase):

    name = __package__

    def ready(self):
        self._register_commands()
        self._register_repositories()

    def _register_commands(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.directory import (
            services,
        )

        bus.add_command_handlers(
            (domain.CreateBbk, services.create_bbk),
            (domain.UpdateBbk, services.update_bbk),
            (domain.DeleteBbk, services.delete_bbk),
        )

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.directory.adapters.db import (
            repository,
        )

        bus.get_uow().register_repositories(('bbk', repository))
