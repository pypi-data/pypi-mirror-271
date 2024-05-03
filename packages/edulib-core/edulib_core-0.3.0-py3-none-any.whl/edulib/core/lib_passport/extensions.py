import importlib


def get_model(*args, **kwargs):
    """Хендлер, для получения моделей плагина Паспорт библиотеки извне, если плагин подключен."""
    model_name = kwargs.get('model_name')
    lib_passport_models = importlib.import_module(
        'edulib.core.lib_passport.models')

    return getattr(lib_passport_models, model_name, None)
