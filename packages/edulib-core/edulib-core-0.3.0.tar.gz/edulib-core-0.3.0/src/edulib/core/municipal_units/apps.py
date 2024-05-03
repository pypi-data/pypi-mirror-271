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

        bus.get_uow().register_repositories(('municipal_units', repository))

    def _register_event_handlers(self):
        from edulib.core import (
            bus,
        )

        from . import (
            services,
        )

        for event, handler in (
            (domain.MunicipalUnitCreated, services.on_municipal_unit_created),
            (domain.MunicipalUnitUpdated, services.on_municipal_unit_updated),
            (domain.MunicipalUnitDeleted, services.on_municipal_unit_deleted),
        ):
            bus.add_event_handler(event, handler)
