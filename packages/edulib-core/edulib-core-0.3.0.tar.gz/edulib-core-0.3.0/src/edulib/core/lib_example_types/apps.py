# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from edulib.core.lib_example_types.domain import (
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
        from edulib.core.lib_example_types.services import (
            handlers,
        )

        bus.add_command_handlers(
            (commands.CreateExampleType, handlers.create_example_type),
            (commands.UpdateExampleType, handlers.update_example_type),
            (commands.DeleteExampleType, handlers.delete_example_type),
        )

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.lib_example_types.adapters.db import (
            repository,
        )

        bus.get_uow().register_repositories(('example_types', repository))
