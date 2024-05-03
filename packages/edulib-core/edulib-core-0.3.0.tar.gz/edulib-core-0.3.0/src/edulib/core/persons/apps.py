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
        self._register_event_handlers()

    def _register_repositories(self):
        from edulib.core import (
            bus,
        )

        from .adapters.db import (
            repository,
        )

        bus.get_uow().register_repositories(('persons', repository))

    def _register_event_handlers(self):
        from edulib.core import (
            bus,
        )

        from . import (
            services,
        )

        for event, handler in (
            (domain.PersonCreated, services.on_person_created),
            (domain.PersonUpdated, services.on_person_updated),
            (domain.PersonDeleted, services.on_person_deleted),
            (domain.PersonDocumentCreated, services.null_handler),
            (domain.PersonDocumentUpdated, services.null_handler),
            (domain.PersonDocumentDeleted, services.null_handler),
        ):
            bus.add_event_handler(event, handler)
