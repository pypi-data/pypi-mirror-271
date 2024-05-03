# flake8: noqa
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LibPassportCleanupDays',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, verbose_name='Внешний ключ', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания', db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения', db_index=True)),
                ('school_id', models.IntegerField(verbose_name='id школы')),
                ('cleanup_date', models.DateField(verbose_name='Дата')),
            ],
            options={
                'db_table': 'library_passport_cleanup_days',
                'verbose_name': 'Санитарные дни',
                'verbose_name_plural': 'Санитарные дни',
            },
        ),
        migrations.AlterUniqueTogether(
            name='libpassportcleanupdays',
            unique_together=set([('school_id', 'cleanup_date')]),
        ),
    ]
