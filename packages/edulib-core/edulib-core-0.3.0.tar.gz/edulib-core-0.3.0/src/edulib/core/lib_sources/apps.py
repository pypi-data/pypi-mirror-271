# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from edulib.core.lib_sources.domain import (
    commands,
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
        from edulib.core.lib_sources.services import (
            handlers,
        )

        bus.add_command_handlers(
            (commands.CreateSource, handlers.create_source),
            (commands.UpdateSource, handlers.update_source),
            (commands.DeleteSource, handlers.delete_source),
        )

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.lib_sources.adapters.db import (
            repository,
        )

        bus.get_uow().register_repositories(('sources', repository))
