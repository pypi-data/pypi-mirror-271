# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from edulib.core.lib_authors.domain import (
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
        from edulib.core.lib_authors.services import (
            handlers,
        )

        bus.add_command_handlers(
            (commands.CreateAuthor, handlers.create_author),
            (commands.UpdateAuthor, handlers.update_author),
            (commands.DeleteAuthor, handlers.delete_author),
        )

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.lib_authors.adapters.db import (
            repository,
        )

        bus.get_uow().register_repositories(('authors', repository))
