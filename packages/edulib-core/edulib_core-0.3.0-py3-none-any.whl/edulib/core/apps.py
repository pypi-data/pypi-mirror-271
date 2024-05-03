# pylint: disable=import-outside-toplevel
from django.apps.config import (
    AppConfig as AppConfigBase,
)


class AppConfig(AppConfigBase):

    name = __package__
    label = 'library_core'

    def ready(self):
        self._bootstrap()

    def _bootstrap(self):
        """Предоставление общей шины ядра."""
        from explicit.messagebus.messagebus import (
            MessageBus,
        )

        from edulib import (
            core,
        )

        from .unit_of_work import (
            UnitOfWork,
        )

        uow = UnitOfWork()
        dependencies = {'uow': uow}
        messagebus = MessageBus(**dependencies)
        core.bus = messagebus
