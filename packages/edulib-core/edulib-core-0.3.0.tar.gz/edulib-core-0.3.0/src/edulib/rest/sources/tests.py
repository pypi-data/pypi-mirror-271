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

from edulib.core.lib_sources.adapters.db import (
    repository,
)
from edulib.core.lib_sources.domain.model import (
    Source,
)


class SourceRestTestCase(TransactionTestCase):
    """Тесты справочника "Источники поступления"."""

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.client = APIClient()
        self.source = {
            'name': 'Федеральный бюджет',
            'school_id': 1,
        }

    def test_create_source(self) -> None:
        """Тест создания источника поступления."""
        response = self.client.post(reverse('sources-list'), self.source)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        for field, value in self.source.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_patch_source(self) -> None:
        """Тест изменения источника поступления."""
        source = repository.add(Source(**self.source))
        updated_fields = {
            'name': 'Муниципальный бюджет',
        }

        response = self.client.patch(reverse('sources-detail', args=[source.id]), updated_fields)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_delete_source(self) -> None:
        """Тест удаления источника поступления."""
        source = repository.add(Source(**self.source))

        response = self.client.delete(reverse('sources-detail', args=[source.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
