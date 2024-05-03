from django.test import (
    TransactionTestCase,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core import (
    bus,
)
from edulib.core.lib_example_types.domain import (
    CreateExampleType,
    DeleteExampleType,
    ExampleType,
    ExampleTypeNotFound,
    ReleaseMethod,
    UpdateExampleType,
)


class ExampleTypeTestCase(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.repository = bus.get_uow().example_types

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.example_type = {
            'name': 'Нехудожественная литература',
            'release_method': ReleaseMethod.ELECTRONIC,
        }

    def test_create_example_type(self) -> None:
        """Тест создания типа библиотечных экземпляров."""
        command = CreateExampleType(**self.example_type)

        example_type = bus.handle(command)

        self.assertIsNotNone(example_type.id)
        db_example_type = self.repository.get_object_by_id(example_type.id)
        for field, value in self.example_type.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(example_type, field), value)
                self.assertEqual(getattr(db_example_type, field), value)

    def test_update_example_type(self) -> None:
        """Тест обновления типа библиотечных экземпляров."""
        example_type = self.repository.add(ExampleType(**self.example_type))
        updated_fields = {
            'name': 'Художественная литература',
            'release_method': ReleaseMethod.PRINTED,
        }
        command = UpdateExampleType(id=example_type.id, **updated_fields)

        result = bus.handle(command)

        db_example_type = self.repository.get_object_by_id(example_type.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(result, field), value)
                self.assertEqual(getattr(db_example_type, field), value)

    def test_delete_example_type(self) -> None:
        """Тест удаления типа библиотечных экземпляров."""
        example_type = self.repository.add(ExampleType(**self.example_type))
        command = DeleteExampleType(id=example_type.id)

        bus.handle(command)

        with self.assertRaises(ExampleTypeNotFound):
            self.repository.get_object_by_id(example_type.id)

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        example_type = self.repository.add(ExampleType(**self.example_type))
        commands_with_errors = (
            (CreateExampleType(name=''), 'name', 'Наименование не может быть пустым'),
            (CreateExampleType(**self.example_type), 'name', 'Такой тип библиотечных экземпляров уже существует'),
            (UpdateExampleType(id=example_type.id, name=''), 'name', 'Наименование не может быть пустым'),
            (UpdateExampleType(id=10_000, name='Комиксы'), 'id', 'Тип библиотечных экземпляров не найден'),
            (DeleteExampleType(id=10_000), 'id', 'Тип библиотечных экземпляров не найден'),
        )

        for command, error, message in commands_with_errors:
            with self.subTest(command=command):
                with self.assertRaises(DomainValidationError) as exc:
                    bus.handle(command)

                self.assertIn(message, exc.exception.message_dict[error])
