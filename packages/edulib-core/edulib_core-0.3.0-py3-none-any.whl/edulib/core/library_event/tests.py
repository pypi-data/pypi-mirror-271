from datetime import (
    date,
)

from django.test import (
    TransactionTestCase,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core import (
    bus,
)
from edulib.core.lib_passport.models import (
    LibPassport,
)
from edulib.core.library_event import (
    domain,
)
from edulib.core.library_event.adapters.db import (
    repository,
)


class EventTestCase(TransactionTestCase):

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        library = LibPassport.objects.create(
            school_id=1,
            name='Библиотека',
            office_id=10,
        )
        self.event = {
            'library_id': library.id,
            'date_begin': date(2023, 1, 20),
            'date_end': date(2023, 1, 25),
            'name': 'Читаем поэмы',
            'participants': 'Учителя, ученики',
            'description': 'Пройдёт мероприятие по чтению поэм',
            'file': None,
            'place': 'Библиотека',
        }

    def test_create_event(self) -> None:
        """Тест создания плана работы библиотеки."""
        command = domain.CreateEvent(**self.event)

        event = bus.handle(command)

        self.assertIsNotNone(event.id)
        db_event = repository.get_object_by_id(event.id)
        self.event.pop('file')
        for field, value in self.event.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(event, field), value)
                self.assertEqual(getattr(db_event, field), value)

    def test_update_event(self) -> None:
        """Тест обновления плана работы библиотеки."""
        event = repository.add(domain.Event(**self.event))
        updated_fields = {
            'date_begin': date(2023, 1, 21),
            'date_end': date(2023, 1, 26),
            'name': 'Читаем стихи',
            'participants': 'Учителя, ученики, родители',
            'description': 'Пройдёт мероприятие по чтению стихов',
            'place': 'Кабинет русского языка',
        }
        command = domain.UpdateEvent(id=event.id, **updated_fields)

        result = bus.handle(command)

        db_event = repository.get_object_by_id(event.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(result, field), value)
                self.assertEqual(getattr(db_event, field), value)

    def test_delete_event(self) -> None:
        """Тест удаления плана работы библиотеки."""
        event = repository.add(domain.Event(**self.event))
        command = domain.DeleteEvent(id=event.id)

        bus.handle(command)

        with self.assertRaises(domain.EventNotFound):
            repository.get_object_by_id(event.id)

    def test_failed_commands(self) -> None:
        """Тест ошибочных команд."""
        event = repository.add(domain.Event(**self.event))
        commands_with_errors = (
            (domain.CreateEvent(**{**self.event, 'library_id': 100}), 'library_id', 'Паспорт библиотеки не найден'),
            (domain.UpdateEvent(id=event.id, library_id=100), 'library_id', 'Паспорт библиотеки не найден'),
        )

        for command, error, message in commands_with_errors:
            with self.subTest(command=command):
                with self.assertRaises(DomainValidationError) as exc:
                    bus.handle(command)

                self.assertIn(message, exc.exception.message_dict[error])
