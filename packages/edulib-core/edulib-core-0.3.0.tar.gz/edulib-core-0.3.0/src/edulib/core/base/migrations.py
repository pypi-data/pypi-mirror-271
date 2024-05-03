"""
Вспомогательные классы и функции для миграций.
"""
# pylint: disable=fixme, abstract-method, protected-access
from contextlib import (
    closing,
    contextmanager,
)

from django.core.serializers import (
    deserialize,
    python as python_serializer_module,
)
from django.db import (
    connection,
)
from django.db.migrations.operations.base import (
    Operation,
)
from django.db.models.aggregates import (
    Max,
)


# TODO: вынести в m3_db_utils, например
def get_objects_from_fixture(file_path, file_type=None,
                             use_natural_foreign_keys=False):
    """Возвращает генератор объектов из файла фикстуры.

    :param basestring file_path: Путь к файлу с данными.
    :param basestring file_type: Тип файла фикстуры (xml, json или yaml).
    :param bool use_natural_foreign_keys: Флаг, указывающий на необходимость
        использовать "естественные" (natural) ключи.

    :rtype: generator
    """
    if file_type is None:
        file_type = file_path[file_path.rfind('.') + 1:]
        if file_type not in ('json', 'xml', 'yaml'):
            raise ValueError('Неподдерживаемый тип файла ' + file_path)

    with open(file_path, 'r', encoding='utf-8') as infile:
        with closing(deserialize(
            file_type,
            infile.read(),
            use_natural_foreign_keys=use_natural_foreign_keys
        )) as objects:
            yield from objects


class LoadFixture(Operation):
    """Операция загрузки фикстур в миграции."""

    reversible = False

    reduces_to_sql = False

    atomic = True

    def __init__(self, file_path, force=False, file_type=None,
                 use_natural_foreign_keys=False):
        """Инициализация экземпляра класса.

        :param str file_path: Путь к файлу.
        :param bool force: Флаг, определяющий необходимость принудительной
            загрузки фикстуры в БД вне зависимости от роутеров БД.
        :param str file_type: Тип файла (json, xml или yaml).
        :param bool use_natural_foreign_keys: Флаг, указывающий на наличие
            в фикстуре "естественных" (natural) ключей.
        """
        self.file_path = file_path
        self.force = force
        self.file_type = file_type
        self.use_natural_foreign_keys = use_natural_foreign_keys

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state,
                          to_state):
        @contextmanager
        def replace_model_loader():
            _get_model = python_serializer_module._get_model
            python_serializer_module._get_model = to_state.apps.get_model
            yield
            python_serializer_module._get_model = _get_model

        db_alias = schema_editor.connection.alias

        with replace_model_loader():
            for obj in get_objects_from_fixture(self.file_path):
                model = obj.object.__class__
                if self.allow_migrate_model(db_alias, model) or self.force:
                    obj.save()


def correct_sequence_value(model, field='id', conn=connection):
    """Корректирует значение последовательности для указанного поля модели.

    Устанавливает в качестве значения последовательности максимальное значение
    указанного поля. Актуально, когда, например, после загрузки какихм-либо
    данных из фикстур становится возможной ситуация, когда при добавлении
    очередной записи последовательность выдаёт значение, которое уже есть в БД.

    :param model: Класс модели.
    :param str field: Имя поля, для последовательности которого выполняется
        корректировка значения.
    :param conn: Подключение к БД, в которой размещена таблица указанной
        модели.
    """
    max_id = model.objects.aggregate(max_id=Max(field))['max_id'] or 1

    cursor = conn.cursor()

    cursor.execute(
        "SELECT setval(pg_get_serial_sequence(%s,%s), %s)", (
            model._meta.db_table,
            model._meta.get_field(field).column,
            max_id,
        )
    )


class CorrectSequence(Operation):
    """Корректирует значение последовательности для указанного поля."""

    reversible = False

    reduces_to_sql = False

    def __init__(self, model_name, force=False):
        self.model_name = model_name
        self.force = force

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state,
                          to_state):
        db_alias = schema_editor.connection.alias
        model = to_state.apps.get_model(app_label, self.model_name)
        if self.allow_migrate_model(db_alias, model) or self.force:
            correct_sequence_value(model, conn=schema_editor.connection)


class ReversibleLoadFixture(LoadFixture):
    """
    Операция загрузки фикстуры с возможностью отката.

    По умолчанию, при откате никаких действий не производится.
    При необходимости удаления данных,
    нужно переопределить метод database_backwards
    """

    reversible = True

    def database_backwards(self, app_label, schema_editor,
                           from_state, to_state):
        """
        Откат операции.

        Если метод переопределен и в нем происходит удаление записей,
        то необходимо после удаления вызывать операцию по корректировке
        последовательности, например:

        model = apps.get_model(app_label, model_name)
        model.objects.get(id=2).delete()
        ReversibleCorrectSequence(model_name).database_forwards(
            app_label, schema_editor, from_state, to_state)
        """


class ReversibleCorrectSequence(CorrectSequence):
    """
    Коррекция последовательности первичных ключей модели с возможностью отката.

    При откате ничего не происходит,
    т.к. операция коррекции будет вызвана до операции, изменяющей данные
    """

    reversible = True

    def database_backwards(self, app_label, schema_editor,  # noqa: D102
                           from_state, to_state):
        pass
