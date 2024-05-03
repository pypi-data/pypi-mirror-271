from datetime import (
    date,
)
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
        cls.repository = bus.get_uow().academic_years
        cls.external_id = str(uuid4())
        cls.initial_data = {
            'external_id': cls.external_id,
            'code': '2001/2002',
            'name': '2001/2001',
            'date_begin': '2001-09-01',
            'date_end': '2002-08-31',
        }
        cls.changed_data = {
            'external_id': cls.external_id,
            'code': '2002/2003',
            'name': '2002/2003',
            'date_begin': '2002-09-01',
            'date_end': '2003-08-31',
        }

    def test_events_created(self):
        bus.handle(domain.AcademicYearCreated(**self.initial_data))

        result = self.repository.get_by_external_id(self.external_id)
        self.assertIsNotNone(result.id)

        for attname, value in self.initial_data.items():
            with self.subTest(attname):
                result_value = getattr(result, attname)
                if isinstance(result_value, date):
                    result_value = result_value.strftime('%Y-%m-%d')
                self.assertEqual(result_value, value)

    def test_events_updated(self):
        self.repository.add(domain.AcademicYear(**self.initial_data))
        self.repository.get_by_external_id(self.external_id)

        bus.handle(domain.AcademicYearUpdated(**self.changed_data))

        result = self.repository.get_by_external_id(self.external_id)

        for attname, value in self.changed_data.items():
            with self.subTest(attname):
                result_value = getattr(result, attname)
                if isinstance(result_value, date):
                    result_value = result_value.strftime('%Y-%m-%d')
                self.assertEqual(result_value, value)

    def test_events_deleted(self):
        self.repository.add(domain.AcademicYear(**self.initial_data))
        self.repository.get_by_external_id(self.external_id)

        bus.handle(domain.AcademicYearDeleted(**self.changed_data))

        with self.assertRaises(domain.AcademicYearNotFound):
            self.repository.get_by_external_id(self.external_id)
