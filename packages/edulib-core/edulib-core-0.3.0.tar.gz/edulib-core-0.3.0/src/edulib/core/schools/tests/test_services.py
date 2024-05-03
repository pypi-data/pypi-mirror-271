import random

from django.test.testcases import (
    TransactionTestCase,
)

from edulib.core import (
    bus,
)
from edulib.core.address import (
    domain as addresses,
)
from edulib.core.municipal_units import (
    domain as municipal_units,
)

from .. import (
    domain,
)


class ServicesTestCase(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.uow = bus.get_uow()

        cls.initial_municipal_unit = cls.uow.municipal_units.add(
            municipal_units.MunicipalUnit(
                external_id=random.getrandbits(63),
                code='Код 1',
                name='Наименование 1',
                constituent_entity='Родительская организация 1',
                okato='36234836001',
                oktmo='36634436111'
            )
        )
        cls.changed_municipal_unit = cls.uow.municipal_units.add(
            municipal_units.MunicipalUnit(
                external_id=random.getrandbits(63),
                code='Код 2',
                name='Наименование 2',
                constituent_entity='Родительская организация 2',
                okato='36234836002',
                oktmo='36634436112'
            )
        )

        cls.repository = cls.uow.schools

        cls.external_id = random.getrandbits(63)

        cls.initial_data = {
            'external_id': cls.external_id,
            'short_name': 'Краткое наименование 1',
            'person_id': 1,
            'status': True,
            'name': 'Наименование 1',
            'inn': '123456789012',
            'kpp': '123456789',
            'okato': '123456789012',
            'oktmo': '12345678901',
            'okpo': '123456789012',
            'ogrn': '123456789012345',
            'institution_type_id': 1,
            'telephone': '88006353535',
            'fax': '88006353535',
            'email': 'oo@example.com',
            'website': 'example.com',
            'parent': None,
            'territory_type_id': 1,
            'municipal_unit_id': cls.initial_municipal_unit.id
        }
        cls.initial_addresses = {
            'f_address': 'г. Казань, ул. Вымышленная, д. 1',
            'u_address': 'г. Казань, ул. Вымышленная, д. 2',
        }
        cls.changed_data = {
            'external_id': cls.external_id,
            'short_name': 'Краткое наименование 2',
            'person_id': 2,
            'status': True,
            'name': 'Наименование 2',
            'inn': '123456789010',
            'kpp': '123456780',
            'okato': '123456789010',
            'oktmo': '12345678900',
            'okpo': '123456789010',
            'ogrn': '123456789012340',
            'institution_type_id': 2,
            'telephone': '88006353530',
            'fax': '88006353530',
            'email': 'oo@example2.com',
            'website': 'example2.com',
            'parent': None,
            'territory_type_id': 2,
            'municipal_unit_id': cls.changed_municipal_unit.id
        }
        cls.changed_addresses = {
            'f_address': 'г. Казань, ул. Вымышленная, д. 2',
            'u_address': 'г. Казань, ул. Вымышленная, д. 1',
        }

    def test_events_created(self):
        bus.handle(domain.SchoolCreated(**self.initial_data | self.initial_addresses))

        result = self.repository.get_by_external_id(self.external_id)
        self.assertIsNotNone(result.id)

        for attname, value in self.initial_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

        for attname, full_value in self.initial_addresses.items():
            address = self.uow.addresses.get_object_by_id(getattr(result, f'{attname}_id'))
            self.assertEqual(address.full, full_value)

    def test_events_updated(self):
        bus.handle(domain.SchoolCreated(**self.initial_data | self.initial_addresses))
        initial_result = self.repository.get_by_external_id(self.external_id)

        initial_address_ids = {
            attname: getattr(initial_result, f'{attname}_id')
            for attname in self.initial_addresses
        }

        bus.handle(domain.SchoolUpdated(**self.changed_data | self.changed_addresses))

        result = self.repository.get_by_external_id(self.external_id)

        for attname, value in self.changed_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

        for attname, full_value in self.changed_addresses.items():
            address = self.uow.addresses.get_object_by_id(getattr(result, f'{attname}_id'))
            self.assertEqual(address.id, initial_address_ids[attname])
            self.assertEqual(address.full, full_value)

    def test_events_deleted(self):
        self.repository.add(domain.School(**self.initial_data | self.initial_addresses))
        initial_result = self.repository.get_by_external_id(self.external_id)
        initial_address_ids = [
            getattr(initial_result, f'{attname}_id') for attname in self.initial_addresses
        ]

        bus.handle(domain.SchoolDeleted(**self.initial_data | self.initial_addresses))

        with self.assertRaises(domain.SchoolNotFound):
            self.repository.get_by_external_id(self.external_id)

        for address_id in initial_address_ids:
            with self.assertRaises(addresses.AddressNotFound):
                self.uow.addresses.get_object_by_id(address_id)
