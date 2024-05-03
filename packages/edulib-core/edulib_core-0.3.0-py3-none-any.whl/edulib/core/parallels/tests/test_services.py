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
        cls.repository = bus.get_uow().parallels
        cls.external_id = 31582727
        cls.initial_data = {
            'external_id': cls.external_id,
            'system_object_id': 0,
            'title': '0',
            'object_status': True
        }
        cls.changed_data = {
            'external_id': cls.external_id,
            'system_object_id': 14,
            'title': 'Курс 1',
            'object_status': True
        }

    def test_events_created(self):
        bus.handle(domain.ParallelCreated(**self.initial_data))

        result = self.repository.get_by_external_id(self.external_id)
        self.assertIsNotNone(result.id)

        for attname, value in self.initial_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

    def test_events_updated(self):
        self.repository.add(domain.Parallel(**self.initial_data))
        self.repository.get_by_external_id(self.external_id)

        bus.handle(domain.ParallelUpdated(**self.changed_data))

        result = self.repository.get_by_external_id(self.external_id)

        for attname, value in self.changed_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

    def test_events_deleted(self):
        self.repository.add(domain.Parallel(**self.initial_data))
        self.repository.get_by_external_id(self.external_id)

        bus.handle(domain.ParallelDeleted(**self.changed_data))

        with self.assertRaises(domain.ParallelNotFound):
            self.repository.get_by_external_id(self.external_id)
