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

        bus.get_uow().register_repositories(('institution_types', repository))

    def _register_event_handlers(self):
        from edulib.core import (
            bus,
        )

        from . import (
            services,
        )

        for event, handler in (
            (domain.InstitutionTypeCreated, services.on_institution_type_created),
            (domain.InstitutionTypeUpdated, services.on_institution_type_updated),
            (domain.InstitutionTypeDeleted, services.on_institution_type_deleted),
        ):
            bus.add_event_handler(event, handler)
