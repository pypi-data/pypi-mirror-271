from django.test import (
    TransactionTestCase,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core import (
    bus,
)
from edulib.core.directory.domain import (
    Bbk,
    BbkNotFound,
    CreateBbk,
    DeleteBbk,
    UpdateBbk,
)


class BbkTestCase(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.repository = bus.get_uow().bbk

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.bbk = {
            'code': '42.11',
            'name': 'Зерновые и зернобобовые культуры',
        }

    def test_create_bbk(self) -> None:
        """Тест создания раздела ББК."""
        command = CreateBbk(**self.bbk)

        bbk = bus.handle(command)

        self.assertIsNotNone(bbk.id)
        db_bbk = self.repository.get_object_by_id(bbk.id)
        for field, value in self.bbk.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(bbk, field), value)
                self.assertEqual(getattr(db_bbk, field), value)

    def test_update_bbk(self) -> None:
        """Тест обновления раздела ББК."""
        bbk = self.repository.add(Bbk(**self.bbk))
        updated_fields = {
            'code': '42.112',
            'name': 'Зерновые культуры',
        }
        command = UpdateBbk(id=bbk.id, **updated_fields)

        result = bus.handle(command)

        db_bbk = self.repository.get_object_by_id(bbk.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(result, field), value)
                self.assertEqual(getattr(db_bbk, field), value)

    def test_delete_bbk(self) -> None:
        """Тест удаления раздела ББК."""
        bbk = self.repository.add(Bbk(**self.bbk))
        command = DeleteBbk(id=bbk.id)

        bus.handle(command)

        with self.assertRaises(BbkNotFound):
            self.repository.get_object_by_id(bbk.id)

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        bbk = self.repository.add(Bbk(**self.bbk))
        commands_with_errors = (
            (CreateBbk(**self.bbk), 'code', 'Такой раздел ББК уже существует'),
            (CreateBbk(code='42.11', name=''), 'name', 'Наименование не может быть пустым'),
            (CreateBbk(code='', name='Зерновые и зернобобовые культуры'), 'code', 'Код не может быть пустым'),
            (UpdateBbk(id=bbk.id, name=''), 'name', 'Наименование не может быть пустым'),
            (UpdateBbk(id=bbk.id, code=''), 'code', 'Код не может быть пустым'),
            (UpdateBbk(id=10_000, code='42.113'), 'id', 'Раздел ББК не найден'),
            (
                CreateBbk(code='42.112', name='Зерновые культуры', parent_id=10_000),
                'parent_id',
                'Раздел ББК не найден',
            ),
            (DeleteBbk(id=10_000), 'id', 'Раздел ББК не найден'),
        )

        for command, error, message in commands_with_errors:
            with self.subTest(command=command):
                with self.assertRaises(DomainValidationError) as exc:
                    bus.handle(command)

                self.assertIn(message, exc.exception.message_dict[error])
