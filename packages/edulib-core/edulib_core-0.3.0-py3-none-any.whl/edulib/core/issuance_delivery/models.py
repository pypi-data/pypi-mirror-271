import datetime

from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)
from edulib.core.lib_registry.models import (
    LibRegistryExample,
)
from edulib.core.readers.models import (
    Reader,
)

from . import (
    domain,
)


class IssuanceDelivery(BaseModel):
    """
    Выдача - сдача экземпляров.
    """
    audit_log = True  # Включение логирования для этой модели

    issuance_date = models.DateField(verbose_name='дата выдачи')
    reader = models.ForeignKey(
        Reader,
        verbose_name='читатель',
        on_delete=models.CASCADE,
    )
    ex_number = models.PositiveSmallIntegerField(
        verbose_name='порядковый номер экземпляра'
    )
    example = models.ForeignKey(
        LibRegistryExample,
        verbose_name='экземпляр',
        on_delete=models.CASCADE,
    )
    department = models.SmallIntegerField(
        choices=domain.DEPARTMENT_CHOICES,
        verbose_name='отдел',
    )

    recipient_id = models.BigIntegerField(
        verbose_name='получатель',
        null=True, blank=True,
        help_text=(
            'Получатель - родитель, который получил '
            'экземпляры за своего ребенка. '
            'ID физлица.'
        )
    )

    fact_delivery_date = models.DateField(
        verbose_name='фактическая дата сдачи',
        null=True,
        blank=True
    )
    special_notes = models.CharField(
        max_length=300,
        verbose_name='особые отметки',
        null=True, blank=True
    )

    MAX_LEASE_DATE = datetime.date(datetime.MAXYEAR, 1, 1)

    def get_number_and_fio(self):
        """
        читатель
        """
        return f'{self.reader.number} - {self.reader.fio()}'

    class Meta:
        db_table = 'lib_iss_del'

    @property
    def expired(self):
        """
        True если срок возврата экземпляра истек

        :rtype: bool
        """

        return self.delivery_date < datetime.datetime.now().date()

    @property
    def expired_date_str(self):
        """
        дата возврата экземпляра

        :rtype: str
        """

        if self.delivery_date == self.MAX_LEASE_DATE:
            return ''
        return self.delivery_date.strftime('%d.%m.%Y')

    def get_expired_message(self, wrap_expired=False):
        if self.expired:
            msg = f'{self.expired_date_str} (просрочен)'
            if wrap_expired:
                msg_wrapped = f'<span style="color:red">{msg}</span>'
                return msg_wrapped
        else:
            msg = (
                self.expired_date_str
                if self.expired_date_str
                else 'неизвестно'
            )
        return msg

    # TODO rename `end_time_lease`
    @property
    def delivery_date(self):
        """
        Дата возврата экземпляра

        :rtype: datetime.date
        """

        try:
            max_days = int(self.example.max_date) or 0
        except (TypeError, ValueError):
            return self.MAX_LEASE_DATE
        return self.issuance_date + datetime.timedelta(days=max_days)

    @property
    def approx_delivery_date(self):
        return self.get_expired_message()

    @property
    def approx_delivery_date_span(self):
        return self.get_expired_message(wrap_expired=True)

    @property
    def author_and_title(self):
        return ' / '.join(
            [
                self.example.lib_reg_entry.authors,
                self.example.lib_reg_entry.book_title,
            ]
        )

    @property
    def title(self):
        return self.example.lib_reg_entry.book_title

    @property
    def authors(self):
        return self.example.lib_reg_entry.authors

    @property
    def classbook_type(self):
        return self.example.classbook_type
