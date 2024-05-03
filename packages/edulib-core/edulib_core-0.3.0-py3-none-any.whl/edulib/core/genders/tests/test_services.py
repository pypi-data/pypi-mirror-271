from uuid import (
    uuid4,
)

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
        cls.repository = bus.get_uow().genders
        cls.external_id = str(uuid4())
        cls.initial_data = {
            'external_id': cls.external_id,
            'code': 'male',
            'name': 'Мужской',
        }
        cls.changed_data = {
            'external_id': cls.external_id,
            'code': 'female',
            'name': 'Женский',
        }

    def test_events_created(self):
        bus.handle(domain.GenderCreated(**self.initial_data))

        result = self.repository.get_by_external_id(self.external_id)
        self.assertIsNotNone(result.id)

        for attname, value in self.initial_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

    def test_events_updated(self):
        self.repository.add(domain.Gender(**self.initial_data))
        self.repository.get_by_external_id(self.external_id)

        bus.handle(domain.GenderUpdated(**self.changed_data))

        result = self.repository.get_by_external_id(self.external_id)

        for attname, value in self.changed_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

    def test_events_deleted(self):
        self.repository.add(domain.Gender(**self.initial_data))
        self.repository.get_by_external_id(self.external_id)

        bus.handle(domain.GenderDeleted(**self.changed_data))

        with self.assertRaises(domain.GenderNotFound):
            self.repository.get_by_external_id(self.external_id)
