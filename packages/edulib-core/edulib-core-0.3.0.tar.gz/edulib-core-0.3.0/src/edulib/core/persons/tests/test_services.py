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
    def test_persons_crud(self):
        initial_data = {
            'external_id': str(uuid4()),
            'surname': 'Александрович',
            'firstname': 'Александр',
            'patronymic': 'Александрович',
            'date_of_birth': '2001-01-01',
            'inn': '5403323050',
            'phone': '88003653535',
            'email': 'aleksandrovichaa@example.com',
            'snils': '00000060001',
            'gender_id': 1,
        }
        event = domain.PersonCreated(**initial_data)
        bus.handle(event)

        initial_person = bus.get_uow().persons.get_by_external_id(initial_data['external_id'])
        self.assertIsNotNone(initial_person.id)

        for attname, value in initial_data.items():
            with self.subTest(attname):
                result = getattr(initial_person, attname)
                if isinstance(result, date):
                    result = result.strftime('%Y-%m-%d')
                self.assertEqual(result, value)

        changed_data = {
            'external_id': initial_data['external_id'],
            'surname': 'Василевич',
            'firstname': 'Василий',
            'patronymic': 'Васильевич',
            'date_of_birth': '2002-02-02',
            'inn': '5403323051',
            'phone': '88003653536',
            'email': 'vasilevichvv@example.com',
            'snils': '00000060002',
            'gender_id': 2,
        }
        event = domain.PersonUpdated(**changed_data)
        bus.handle(event)

        changed_person = bus.get_uow().persons.get_by_external_id(changed_data['external_id'])
        self.assertIsNotNone(initial_person.id)

        for attname, value in changed_data.items():
            with self.subTest(attname):
                result = getattr(changed_person, attname)
                if isinstance(result, date):
                    result = result.strftime('%Y-%m-%d')
                self.assertEqual(result, value)

        event = domain.PersonDeleted(**changed_data)
        bus.handle(event)

        with self.assertRaises(domain.PersonNotFound):
            bus.get_uow().persons.get_by_external_id(changed_data['external_id'])
