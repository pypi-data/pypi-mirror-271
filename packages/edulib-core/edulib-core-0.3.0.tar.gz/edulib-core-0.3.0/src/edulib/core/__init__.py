import logging


default_app_config = f'{__package__}.apps.AppConfig'

bus: 'MessageBus'

logger = logging.getLogger(__name__)
