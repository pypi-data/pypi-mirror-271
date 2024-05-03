from uuid import (
    UUID,
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
        cls.uow = bus.get_uow()
        cls.repository = cls.uow.addresses

        def get_hex_str():
            return str(uuid4().hex)

        cls.initial_data = {
            'place': get_hex_str(),
            'street': get_hex_str(),
            'house': get_hex_str(),
            'house_num': '1',
            'house_corps': 'Б',
            'flat': '11',
            'zip_code': '101000',
            'full': '101000, г. Москва, ул. Советская, д. 1 к. Б'
        }
        cls.changed_data = {
            'place': get_hex_str(),
            'street': get_hex_str(),
            'house': get_hex_str(),
            'house_num': '2',
            'house_corps': 'В',
            'flat': '12',
            'zip_code': '101010',
            'full': '101010, г. Москва, ул. Советская, д. 2 к. В'
        }

    def test_commands_create(self):
        result_id = bus.handle(domain.CreateAddress(**self.initial_data)).id
        result = self.repository.get_object_by_id(result_id)

        self.assertIsNotNone(result.id)
        for attname, value in self.initial_data.items():
            with self.subTest(attname):
                if attname in ['place', 'street', 'house']:
                    value = UUID(value)

                self.assertEqual(getattr(result, attname), value)

    def test_commands_update(self):
        result_id = bus.handle(domain.CreateAddress(**self.initial_data)).id

        bus.handle(domain.UpdateAddress(id=result_id, **self.changed_data))
        result = self.repository.get_object_by_id(result_id)

        for attname, value in self.changed_data.items():
            with self.subTest(attname):
                if attname in ['place', 'street', 'house']:
                    value = UUID(value)

                self.assertEqual(getattr(result, attname), value)

    def test_commands_delete(self):
        result_id = bus.handle(domain.CreateAddress(**self.initial_data)).id

        bus.handle(domain.DeleteAddress(id=result_id, **self.changed_data))

        with self.assertRaises(domain.AddressNotFound):
            self.repository.get_object_by_id(result_id)
