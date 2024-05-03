from django.test import (
    TransactionTestCase,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core import (
    bus,
)
from edulib.core.lib_publishings.adapters.db import (
    repository,
)
from edulib.core.lib_publishings.domain.commands import (
    CreatePublishing,
    DeletePublishing,
    UpdatePublishing,
)
from edulib.core.lib_publishings.domain.model import (
    Publishing,
    PublishingNotFound,
)


class PublishingTestCase(TransactionTestCase):

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.publishing = {
            'name': 'Питер',
        }

    def test_create_publishing(self) -> None:
        """Тест создания издательства."""
        command = CreatePublishing(**self.publishing)

        publishing = bus.handle(command)

        self.assertIsNotNone(publishing.id)
        db_publishing = repository.get_object_by_id(publishing.id)
        for field, value in self.publishing.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(publishing, field), value)
                self.assertEqual(getattr(db_publishing, field), value)

    def test_update_publishing(self) -> None:
        """Тест обновления издательства."""
        publishing = repository.add(Publishing(**self.publishing))
        updated_fields = {
            'name': 'БХВ',
        }
        command = UpdatePublishing(id=publishing.id, **updated_fields)

        result = bus.handle(command)

        db_publishing = repository.get_object_by_id(publishing.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(result, field), value)
                self.assertEqual(getattr(db_publishing, field), value)

    def test_delete_publishing(self) -> None:
        """Тест удаления издательства."""
        publishing = repository.add(Publishing(**self.publishing))
        command = DeletePublishing(id=publishing.id)

        bus.handle(command)

        with self.assertRaises(PublishingNotFound):
            repository.get_object_by_id(publishing.id)

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        publishing = repository.add(Publishing(**self.publishing))
        commands_with_errors = (
            (CreatePublishing(**self.publishing), 'Такое издательство уже существует'),
            (CreatePublishing(name=''), 'Наименование не может быть пустым'),
            (UpdatePublishing(id=publishing.id, name=''), 'Наименование не может быть пустым'),
        )

        for command, error in commands_with_errors:
            with self.subTest(command=command):
                with self.assertRaises(DomainValidationError) as err:
                    bus.handle(command)

                self.assertIn(error, err.exception.message_dict['name'])
