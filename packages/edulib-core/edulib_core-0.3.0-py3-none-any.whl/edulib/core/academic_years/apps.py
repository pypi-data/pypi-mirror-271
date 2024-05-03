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

        bus.get_uow().register_repositories(('academic_years', repository))

    def _register_event_handlers(self):
        from edulib.core import (
            bus,
        )

        from . import (
            services,
        )

        for event, handler in (
            (domain.AcademicYearCreated, services.on_academic_year_created),
            (domain.AcademicYearUpdated, services.on_academic_year_updated),
            (domain.AcademicYearDeleted, services.on_academic_year_deleted),
        ):
            bus.add_event_handler(event, handler)
