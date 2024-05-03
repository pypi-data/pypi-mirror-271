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

from edulib.core.lib_publishings.adapters.db import (
    repository,
)
from edulib.core.lib_publishings.domain.model import (
    Publishing,
)


class PublishingRestTestCase(TransactionTestCase):
    """Тесты справочника "Издательства"."""

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.client = APIClient()
        self.publishing = {
            'name': 'Питер',
        }

    def test_create_publishing(self) -> None:
        """Тест создания издательства."""
        response = self.client.post(reverse('publishings-list'), self.publishing)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        for field, value in self.publishing.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_patch_publishing(self) -> None:
        """Тест изменения издательства."""
        publishing = repository.add(Publishing(**self.publishing))
        updated_fields = {
            'name': 'БХВ',
        }

        response = self.client.patch(reverse('publishings-detail', args=[publishing.id]), updated_fields)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_delete_publishing(self) -> None:
        """Тест удаления издательства."""
        publishing = repository.add(Publishing(**self.publishing))

        response = self.client.delete(reverse('publishings-detail', args=[publishing.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
