from django.test import (
    TransactionTestCase,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core import (
    bus,
)
from edulib.core.lib_authors.adapters.db import (
    repository,
)
from edulib.core.lib_authors.domain.commands import (
    CreateAuthor,
    DeleteAuthor,
    UpdateAuthor,
)
from edulib.core.lib_authors.domain.model import (
    Author,
    AuthorNotFound,
)


class AuthorTestCase(TransactionTestCase):

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.author = {
            'name': 'Пушкин А. С.',
        }

    def test_create_author(self) -> None:
        """Тест создания автора."""
        command = CreateAuthor(**self.author)

        author = bus.handle(command)

        self.assertIsNotNone(author.id)
        db_author = repository.get_object_by_id(author.id)
        for field, value in self.author.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(author, field), value)
                self.assertEqual(getattr(db_author, field), value)

    def test_create_with_existing_name(self) -> None:
        """Тест создания автора с существующим именем."""
        repository.add(Author(**self.author))
        command = CreateAuthor(**self.author)

        with self.assertRaises(DomainValidationError) as err:
            bus.handle(command)

        self.assertIn(
            'Такой автор уже существует',
            err.exception.message_dict['name'],
        )

    def test_update_author(self) -> None:
        """Тест изменения автора."""
        author = repository.add(Author(name='Пушкин А. М.'))
        updated_fields = {
            'name': 'Пушкин А. С.',
        }
        command = UpdateAuthor(id=author.id, **updated_fields)

        result = bus.handle(command)

        db_author = repository.get_object_by_id(author.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(result, field), value)
                self.assertEqual(getattr(db_author, field), value)

    def test_update_with_existing_name(self) -> None:
        """Тест изменения автора с существующим именем."""
        repository.add(Author(name='пушкин а. с.'))
        author = repository.add(Author(name='Пушкин А. М.'))
        command = UpdateAuthor(id=author.id, **self.author)

        with self.assertRaises(DomainValidationError) as err:
            bus.handle(command)

        self.assertIn(
            'Такой автор уже существует',
            err.exception.message_dict['name'],
        )

    def test_delete_author(self) -> None:
        """Тест удаления автора."""
        author = repository.add(Author(name='Пушкин А. С.'))
        command = DeleteAuthor(id=author.id)

        bus.handle(command)

        with self.assertRaises(AuthorNotFound):
            repository.get_object_by_id(author.id)
