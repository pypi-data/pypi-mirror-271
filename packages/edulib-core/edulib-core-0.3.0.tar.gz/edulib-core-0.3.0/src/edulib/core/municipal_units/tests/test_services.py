import random

from django.test.testcases import (
    TransactionTestCase,
)

from edulib.core import (
    bus,
)

from .. import (
    domain,
)


class ServicesTestCase(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.repository = bus.get_uow().municipal_units

        cls.external_id = random.getrandbits(63)

        cls.parent_data = {
            'external_id': random.getrandbits(63),
            'code': 'Код родителя 1',
            'name': 'Наименование родителя 1',
            'okato': '123456789010',
            'oktmo': '12345678900',
            'constituent_entity': 'Москва',
        }

        cls.initial_data = {
            'external_id': cls.external_id,
            'code': 'Код 1',
            'name': 'Наименование 1',
            'okato': '123456789012',
            'oktmo': '12345678901',
            'constituent_entity': 'Санкт-Петербург'
        }
        cls.changed_data = {
            'external_id': cls.external_id,
            'code': 'Код 2',
            'name': 'Наименование 2',
            'okato': '123456789015',
            'oktmo': '12345678905',
            'constituent_entity': 'Севастополь'
        }

    def test_events_created(self):
        parent = self.repository.add(domain.MunicipalUnit(**self.parent_data))

        bus.handle(domain.MunicipalUnitCreated(parent_id=parent.id, **self.initial_data))

        result = self.repository.get_by_external_id(self.external_id)
        self.assertIsNotNone(result.id)

        for attname, value in self.initial_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

        self.assertEqual(result.parent, parent)

    def test_events_updated(self):
        parent = self.repository.add(domain.MunicipalUnit(**self.parent_data))
        self.repository.add(domain.MunicipalUnit(parent=parent, **self.initial_data))
        self.repository.get_by_external_id(self.external_id)

        bus.handle(domain.MunicipalUnitUpdated(parent_id=parent.id, **self.changed_data))

        result = self.repository.get_by_external_id(self.external_id)

        for attname, value in self.changed_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

        self.assertEqual(result.parent, parent)

    def test_events_updated_no_parent(self):
        parent = self.repository.add(domain.MunicipalUnit(**self.parent_data))
        self.repository.add(domain.MunicipalUnit(parent=parent, **self.initial_data))
        self.repository.get_by_external_id(self.external_id)

        bus.handle(domain.MunicipalUnitUpdated(parent_id=None, **self.changed_data))

        result = self.repository.get_by_external_id(self.external_id)

        for attname, value in self.changed_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

        self.assertIsNone(result.parent)

    def test_events_deleted(self):
        parent = self.repository.add(domain.MunicipalUnit(**self.parent_data))
        self.repository.add(domain.MunicipalUnit(parent=parent, **self.initial_data))
        self.repository.get_by_external_id(self.external_id)

        bus.handle(domain.MunicipalUnitDeleted(**self.changed_data))

        with self.assertRaises(domain.MunicipalUnitNotFound):
            self.repository.get_by_external_id(self.external_id)
