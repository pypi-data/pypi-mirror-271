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

from edulib.core.lib_example_types.adapters.db import (
    repository,
)
from edulib.core.lib_example_types.domain import (
    ExampleType,
    ReleaseMethod,
)


class ExampleTypeTestCase(TransactionTestCase):
    """Тесты справочника "Типы библиотечных экземпляров"."""

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.client = APIClient()
        self.example_type = {
            'name': 'Нехудожественная литература',
            'release_method': ReleaseMethod.ELECTRONIC,
        }

    def test_create_example_type(self) -> None:
        """Тест создания типа библиотечного экземпляра."""
        response = self.client.post(reverse('example-types-list'), self.example_type)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        for field, value in self.example_type.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_update_example_type(self) -> None:
        """Тест обновления типа библиотечного экземпляра."""
        example_type = repository.add(ExampleType(**self.example_type))
        updated_fields = {
            'name': 'Художественная литература',
            'release_method': ReleaseMethod.PRINTED,
        }

        response = self.client.patch(reverse('example-types-detail', args=[example_type.id]), updated_fields)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_delete_example_type(self) -> None:
        """Тест удаления типа библиотечного экземпляра."""
        example_type = repository.add(ExampleType(**self.example_type))

        response = self.client.delete(reverse('example-types-detail', args=[example_type.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
