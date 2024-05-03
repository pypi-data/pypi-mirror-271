import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MunicipalUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')),
                ('external_id', models.BigIntegerField(db_index=True, verbose_name='Глобальный идентификатор')),
                ('code', models.CharField(max_length=20, verbose_name='Код')),
                ('name', models.TextField(null=True, verbose_name='Наименование')),
                ('constituent_entity', models.CharField(max_length=200, verbose_name='Наименование субъекта РФ')),
                ('okato', models.CharField(max_length=12, null=True, verbose_name='ОКАТО')),
                ('oktmo', models.CharField(max_length=11, null=True, verbose_name='ОКТМО')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='municipal_units.municipalunit', verbose_name='Родительская организация')),
            ],
            options={
                'verbose_name': 'Муниципальная единица',
                'verbose_name_plural': 'Муниципальные единицы',
                'db_table': 'municipal_unit',
            },
        ),
    ]
