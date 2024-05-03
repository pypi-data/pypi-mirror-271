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
    def test_classes_crud(self):
        initial_data = {
            'external_id': str(uuid4()),
            'school_id': 1,
            'name': 'Класс 1',
            'parallel_id': 1,
            'letter': 'М',
            'teacher_id': 1,
            'academic_year_id': 1,
            'open_at': '2001-01-01',
            'close_at': '2101-01-01',
        }
        event = domain.ClassYearCreated(**initial_data)
        bus.handle(event)

        initial_class = bus.get_uow().classyears.get_by_external_id(initial_data['external_id'])
        self.assertIsNotNone(initial_class.id)

        for attname, value in initial_data.items():
            with self.subTest(attname):
                result = getattr(initial_class, attname)
                if isinstance(result, date):
                    result = result.strftime('%Y-%m-%d')
                self.assertEqual(result, value)

        changed_data = {
            'external_id': initial_data['external_id'],
            'school_id': 2,
            'name': 'Класс 2',
            'parallel_id': 2,
            'letter': 'Н',
            'teacher_id': 2,
            'academic_year_id': 2,
            'open_at': '2002-01-01',
            'close_at': '2102-01-01',
        }
        event = domain.ClassYearUpdated(**changed_data)
        bus.handle(event)

        changed_class = bus.get_uow().classyears.get_by_external_id(changed_data['external_id'])
        self.assertIsNotNone(initial_class.id)

        for attname, value in changed_data.items():
            with self.subTest(attname):
                result = getattr(changed_class, attname)
                if isinstance(result, date):
                    result = result.strftime('%Y-%m-%d')
                self.assertEqual(result, value)

        event = domain.ClassYearDeleted(**changed_data)
        bus.handle(event)

        with self.assertRaises(domain.ClassYearNotFound):
            bus.get_uow().classyears.get_by_external_id(changed_data['external_id'])
