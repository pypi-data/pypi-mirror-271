# pylint: disable=import-outside-toplevel
from django.apps import (
    AppConfig as AppConfigBase,
)

from edulib.core.library_event import (
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
        from edulib.core.library_event import (
            services,
        )

        bus.add_command_handlers(
            (domain.CreateEvent, services.create_event),
            (domain.UpdateEvent, services.update_event),
            (domain.DeleteEvent, services.delete_event),
        )

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )
        from edulib.core.library_event.adapters.db import (
            repository,
        )

        bus.get_uow().register_repositories(('events', repository))
