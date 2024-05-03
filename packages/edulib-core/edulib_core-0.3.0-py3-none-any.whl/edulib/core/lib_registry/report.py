import datetime
import os

from edureporter import (
    AbstractDataProvider,
    AbstractReportBuilder,
)
from edureporter.reporter import (
    SimpleReporter,
)
from edureporter.utils import (
    adjust_row_height_arial,
)


class LibraryCardProvider(AbstractDataProvider):

    """Провайдер данных "Библиотечной карточки"."""


class LibraryCardBuilder(AbstractReportBuilder):

    """Билдер отчета "Библиотечная карточка"."""

    def __init__(self, provider, adapter, report, params):
        super().__init__()
        self.provider = provider
        self.report = report
        self.report_dict = params['report_dict']
        self.school = params['school']
        self.extension = params['extension']

    def build(self):
        self.report_dict['organization'] = self.school
        self.report_dict['date'] = datetime.datetime.now().strftime('%d.%m.%Y')
        if self.extension == '.xls':
            page = self.report.get_section('page')
            page.flush(self.report_dict)
            adjust_row_height_arial(page, 1, 2, self.school, font_size=11)
        else:
            return self.report_dict


class Reporter(SimpleReporter):

    """Построитель отчета библиотечной карточки."""

    data_provider_class = LibraryCardProvider
    builder_class = LibraryCardBuilder

    def set_file_and_url(self):
        self.extension = self.builder_params['report_dict']['file_format']
        return super().set_file_and_url()

    def get_template(self, default_base_name='report'):
        template_name = 'lib_registry_card'
        self.extension = self.builder_params['report_dict']['file_format']
        self.template_file_path = os.path.join(
            os.path.dirname(__file__), 'templates',
            'reports', template_name + self.extension
        )
        return super().get_template(default_base_name='report')
