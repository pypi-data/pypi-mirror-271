# pylint: disable=global-statement
from typing import (
    Union,
)

from .config import (
    Config,
)


_config: Union[Config, None] = None


def set_config(config: Config) -> Config:
    global _config

    assert isinstance(config, Config), f'{type(config)} is not Config'

    _config = config

    return _config


def get_config() -> Config:
    assert _config is not None, 'Не произведена настройка приложения'
    return _config
