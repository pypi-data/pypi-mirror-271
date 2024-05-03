"""
Created on 19.01.2015
@author: salin
"""
# pylint: disable=unused-variable, c-extension-no-member, unnecessary-comprehension, consider-using-f-string

import sys
import time
from multiprocessing import (
    Manager,
    Process,
    Queue,
    Value,
)
from urllib.parse import (
    urljoin,
)

import requests
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)
from django.core.management.base import (
    BaseCommand,
)
from lxml import (
    etree,
)

from edulib.core.base.files import (
    get_abspath,
)
from edulib.core.lib_udc.models import (
    LibraryUDC,
)
from edulib.core.utils.parse import (
    CSVReader,
    CSVWriter,
)


class Command(BaseCommand):
    """Загрузка справочника по УДК (http://teacode.com/online/udc/index.html)."""

    TOTAL = 121655
    """Общее число кодов для расчета оставшегося времени"""
    PROCESS_COUNT = 4
    """Количество процессов"""
    TOP_URL = 'http://teacode.com/online/udc/index.html'

    def add_arguments(self, parser):
        """Определение аргументов команды."""
        parser.add_argument(
            'action',
            choices=['import', 'export'],
            help='Выберите "import" или "export"'
        )
        parser.add_argument(
            '-f',
            '--file',
            dest='filename',
            help='Filename',
            metavar='FILE'
        )

    def handle(self, *args, **options):
        """Выполнение действий команды."""
        file_path = options['filename']
        action = options['action']
        if not file_path or action not in ['import', 'export']:
            BaseCommand.print_help(self, *sys.argv[:2])
            return

        if action == 'import':
            self.import_udc(file_path)
        else:
            self.export_udc(file_path)

    def import_udc(self, file_path):
        """Импорт УДК в CSV."""

        self.stdout.write('Starting import...\n')
        # Очередь для URL
        urls = Queue()
        urls.put(self.TOP_URL)
        # Очередь для УДК
        manager = Manager()
        udcs = manager.list()
        # Количество распарсенных кодов
        ready = Value('i', 0)

        procs = []
        for i in range(self.PROCESS_COUNT):
            procs.append(Process(target=self.parse_html, args=(urls, udcs, ready)))
        for proc in procs:
            proc.start()
        for proc in procs:
            proc.join()

        udcs.sort()
        with open(get_abspath(file_path), 'wb') as f:
            writer = CSVWriter(f)
            # Шапка CSV
            header_row = ('Код', 'Описание')
            writer.writerow(header_row)
            writer.writerows(udcs)
        self.stdout.write('\nImport has been completed.\n')

    def parse_html(self, urls, udcs, ready):
        """Получение содержимого и парсинг HTML."""
        # Для избежания ситуации, когда первый процесс еще не успел
        # добавить url в очередь, а второй обнаружил пусто и завершился
        if urls.empty():
            time.sleep(3)

        while not urls.empty():
            url = urls.get()
            session = requests.Session()
            response = session.get(url)
            if response.status_code != 200:
                self.stdout.write(f'\nError! URL {url} is not available.\n')
                continue

            tree = etree.fromstring(  # noqa: S320
                response.text,
                parser=etree.HTMLParser(encoding='utf8')
            )

            table = tree.xpath('//table//table')[0]
            for row in table.xpath('.//tr')[1:-1]:
                cols = [v for v in row.xpath('./td')[:-1]]
                if not cols[0].xpath('.//text()'):
                    continue

                udc = [
                    r.xpath('.//text()')[0].strip().replace('\r', '').replace('\n', '')
                    if r.xpath('.//text()') and not r.xpath('.//text()')[0].startswith('$=')
                    else ''
                    for r in cols
                ]

                udcs.append(udc)
                ready.value += 1

                link = cols[0].xpath('.//a/@href')
                if link:
                    urls.put(urljoin(url, link[0]))

            self.stdout.write(
                '\rProgress: {0:.2%}. URL queue size: {1:d}'.format(
                    ready.value / float(self.TOTAL),
                    int(urls.qsize())
                ))
            self.stdout.flush()

    def export_udc(self, file_path):
        """Экспорт УДК из CSV в БД."""
        self.stdout.write('Starting export...\n')
        with open(get_abspath(file_path), 'rb') as f:
            reader = CSVReader(f)
            next(reader)
            udcs = []
            for row in reader:
                # Пропускаем коды без описания (они являются исключенными)
                if row[1]:
                    # В кодах больше 30 символов может быть лишняя информация
                    code = row[0].partition(' ')[0] if len(row[0]) > 30 else row[0]
                    udcs.append(
                        LibraryUDC(code=code, name=row[1])
                    )
            try:
                LibraryUDC.objects.bulk_create(udcs)
            except DjangoValidationError as e:
                self.stdout.write('\n{0}\n'.format(e))
        self.stdout.write('\nExport has been completed.\n')
