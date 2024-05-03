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
            name='ClassYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')),
                ('external_id', models.CharField(db_index=True, max_length=36, verbose_name='Глобальный идентификатор')),
                ('school_id', models.BigIntegerField(verbose_name='Организация')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('parallel_id', models.BigIntegerField(verbose_name='Параллель')),
                ('letter', models.CharField(blank=True, max_length=20, null=True, verbose_name='Литер')),
                ('teacher_id', models.BigIntegerField(blank=True, null=True, verbose_name='Идентификатор учителя')),
                ('academic_year_id', models.BigIntegerField(verbose_name='Идентификатор академического года')),
                ('open_at', models.DateField(blank=True, null=True, verbose_name='Дата открытия класса')),
                ('close_at', models.DateField(blank=True, null=True, verbose_name='Дата закрытия класса')),
            ],
            options={
                'verbose_name': 'Класс',
                'verbose_name_plural': 'Классы',
                'db_table': 'class_year',
            },
        ),
    ]
