from django.core.management import (
    BaseCommand,
)
from django.db import (
    transaction,
)

from edulib.core.lib_authors.models import (
    LibraryAuthors,
)


class Command(BaseCommand):
    """
    Удаляет символ переноса каретки из справочника по авторам.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix', type=bool, default=False,
            help='Применить скрипт для изменения записей'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        broken_authors = LibraryAuthors.objects.filter(name__contains='\n')
        self.stdout.write(
            f'Найдено {broken_authors.count()} авторов с символом переноса.'
        )
        cnt = 0
        for author in broken_authors:
            author.name = author.name.replace('\n', ' ')
            self.stdout.write(f'{author.id}: {author.name}')
            if options['fix']:
                author.save()
            cnt += 1

        self.stdout.write(
            f'Исправлено {cnt} авторов с символом переноса.'
        )
