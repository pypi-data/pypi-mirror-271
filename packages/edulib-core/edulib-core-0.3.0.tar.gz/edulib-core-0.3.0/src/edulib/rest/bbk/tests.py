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

from edulib.core.directory.adapters.db import (
    repository,
)
from edulib.core.directory.domain import (
    Bbk,
)


class RestBbkTestCase(TransactionTestCase):
    """Тесты справочника "Разделы ББК"."""

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.client = APIClient()
        self.bbk = {
            'code': '42.11',
            'name': 'Зерновые и зернобобовые культуры',
        }

    def test_create_bbk(self) -> None:
        """Тест создания раздела ББК."""
        response = self.client.post(reverse('bbk-list'), self.bbk)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        for field, value in self.bbk.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_patch_bbk(self) -> None:
        """Тест изменения раздела ББК."""
        bbk = repository.add(Bbk(**self.bbk))
        updated_fields = {
            'code': '42.112',
            'name': 'Зерновые культуры',
        }

        response = self.client.patch(reverse('bbk-detail', args=[bbk.id]), updated_fields)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_delete_bbk(self) -> None:
        """Тест удаления раздела ББК."""
        bbk = repository.add(Bbk(**self.bbk))

        response = self.client.delete(reverse('bbk-detail', args=[bbk.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
