from django.apps.config import (
    AppConfig as AppConfigBase,
)


class AppConfig(AppConfigBase):

    name = __package__
    label = 'library_scanned_copy'
