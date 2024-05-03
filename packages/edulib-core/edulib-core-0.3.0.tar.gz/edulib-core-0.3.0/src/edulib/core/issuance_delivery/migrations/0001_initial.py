# flake8: noqa
import django
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('readers', '0001_initial'),
        ('lib_registry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssuanceDelivery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, verbose_name='Внешний ключ', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания', db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения', db_index=True)),
                ('issuance_date', models.DateField(verbose_name='дата выдачи')),
                ('ex_number', models.PositiveSmallIntegerField(verbose_name='порядковый номер экземпляра')),
                ('department', models.SmallIntegerField(verbose_name='отдел', choices=[(0, 'абонемент'), (1, 'читальный зал')])),
                ('fact_delivery_date', models.DateField(null=True, verbose_name='фактическая дата сдачи', blank=True)),
                ('special_notes', models.CharField(max_length=300, null=True, verbose_name='особые отметки', blank=True)),
                ('example', models.ForeignKey(verbose_name='экземпляр', to='lib_registry.LibRegistryExample',
                                              on_delete=django.db.models.deletion.CASCADE)),
                ('reader', models.ForeignKey(verbose_name='читатель', to='readers.Reader',
                                             on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'lib_iss_del',
            },
        ),
    ]
