# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from edulib.core.lib_publishings.domain import (
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
        from edulib.core.lib_publishings.services import (
            handlers,
        )

        bus.add_command_handlers(
            (commands.CreatePublishing, handlers.create_publishing),
            (commands.UpdatePublishing, handlers.update_publishing),
            (commands.DeletePublishing, handlers.delete_publishing),
        )

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.lib_publishings.adapters.db import (
            repository,
        )

        bus.get_uow().register_repositories(('publishings', repository))
