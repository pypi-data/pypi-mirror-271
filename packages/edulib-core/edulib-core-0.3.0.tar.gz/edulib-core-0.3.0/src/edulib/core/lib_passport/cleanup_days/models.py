from django.core.exceptions import (
    ValidationError,
)
from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)


class LibPassportCleanupDays(BaseModel):
    audit_log = True

    school_id = models.IntegerField(verbose_name='id школы')
    cleanup_date = models.DateField(verbose_name='Дата')

    def save(self, *args, **kwargs):
        if LibPassportCleanupDays.objects.filter(
            cleanup_date=self.cleanup_date, school_id=self.school_id
        ).exclude(pk=self.pk).exists():
            raise ValidationError('Такая дата уже существует!')
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'library_passport_cleanup_days'
        verbose_name = 'Санитарные дни'
        verbose_name_plural = 'Санитарные дни'
        unique_together = ('school_id', 'cleanup_date')
