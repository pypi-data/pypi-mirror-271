from django.test import (
    TransactionTestCase,
)
from django.urls import (
    reverse,
)
from rest_framework import (
    status,
)
from rest_framework.test import (
    APIClient,
)

from edulib.core.lib_authors.adapters.db import (
    repository,
)
from edulib.core.lib_authors.domain.model import (
    Author,
)


class AuthorTestCase(TransactionTestCase):
    """Тесты справочника "Авторы"."""

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.client = APIClient()
        self.author = {
            'name': 'Пушкин А. С.',
        }

    def test_create_author(self) -> None:
        """Тест создания автора."""
        response = self.client.post(reverse('authors-list'), self.author)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        for field, value in self.author.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_patch_author(self) -> None:
        """Тест изменения автора."""
        author = repository.add(Author(**self.author))
        updated_fields = {
            'name': 'Пушкин А. М.',
        }

        response = self.client.patch(reverse('authors-detail', args=[author.id]), updated_fields)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_delete_author(self) -> None:
        """Тест удаления автора."""
        author = repository.add(Author(**self.author))

        response = self.client.delete(reverse('authors-detail', args=[author.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
