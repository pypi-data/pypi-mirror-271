# Ядро продукта "Библиотека"
## Подключение

requirements:

    edulib-core>=1.0.0,<2.0

settings:

    INSTALLED_APPS = [
        ...
        'edulib.core',
        'edulib.core.directory',
        'edulib.core.issuance_delivery',
        'edulib.core.lib_authors',
        'edulib.core.lib_example_types',
        'edulib.core.lib_passport',
        'edulib.core.lib_passport.cleanup_days',
        'edulib.core.lib_passport.documents',
        'edulib.core.lib_publishings',
        'edulib.core.lib_registry',
        'edulib.core.lib_sources',
        'edulib.core.lib_udc',
        'edulib.core.library_event',
        'edulib.core.readers',
        'edulib.core.scanned_copy',

        'edulib.rest',

        ...
    ]

## Запуск тестов
    $ tox
