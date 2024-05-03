import datetime
from uuid import (
    uuid4,
)

from dateutil.relativedelta import (
    relativedelta,
)
from django.test.testcases import (
    TransactionTestCase,
)

from edulib.core import (
    bus,
)
from edulib.core.classyears import (
    domain as classyears,
)
from edulib.core.persons import (
    domain as persons,
)

from .. import (
    domain,
)


class ServicesTestCase(TransactionTestCase):

    def setUp(self) -> None:
        self.uow = bus.get_uow()

        classyear_data = {
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
        bus.handle(classyears.ClassYearCreated(**classyear_data))
        self.classyear: classyears.ClassYear = self.uow.classyears.get_by_external_id(classyear_data['external_id'])

        person_data = {
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
        bus.handle(persons.PersonCreated(**person_data))
        self.person: persons.Person = self.uow.persons.get_by_external_id(person_data['external_id'])

    def test_pupils_crud(self):
        initial_data = {
            'person_id': self.person.external_id,
            'external_id': str(uuid4()),
            'training_begin_date': datetime.date.today(),
            'training_end_date': datetime.date.today() + relativedelta(days=365),
            'class_external_id': self.classyear.external_id,
            'school_id': 1
        }
        bus.handle(domain.PupilCreated(**initial_data))
        initial_pupil = self.uow.pupils.get_by_external_id(initial_data['external_id'])

        self.assertIsNotNone(initial_pupil.id)
        self.assertEqual(initial_pupil.training_begin_date, initial_data['training_begin_date'])
        self.assertEqual(initial_pupil.training_end_date, initial_data['training_end_date'])
        self.assertEqual(initial_pupil.school_id, initial_data['school_id'])
        self.assertEqual(initial_pupil.class_year_id, self.classyear.id)

        changed_data = {
            'person_id': self.person.external_id,
            'external_id': initial_data['external_id'],
            'training_begin_date': datetime.date.today() + relativedelta(days=10),
            'training_end_date': datetime.date.today() + relativedelta(days=375),
            'class_external_id': self.classyear.external_id,
            'school_id': 2
        }
        event = domain.PupilUpdated(**changed_data)
        bus.handle(event)

        changed_pupil = self.uow.pupils.get_by_external_id(changed_data['external_id'])

        self.assertIsNotNone(changed_pupil.id)
        self.assertEqual(changed_pupil.training_begin_date, changed_data['training_begin_date'])
        self.assertEqual(changed_pupil.training_end_date, changed_data['training_end_date'])
        self.assertEqual(changed_pupil.school_id, changed_data['school_id'])
        self.assertEqual(changed_pupil.class_year_id, self.classyear.id)

        event = domain.PupilDeleted(**changed_data)
        bus.handle(event)

        with self.assertRaises(domain.PupilNotFound):
            self.uow.pupils.get_by_external_id(changed_data['external_id'])
