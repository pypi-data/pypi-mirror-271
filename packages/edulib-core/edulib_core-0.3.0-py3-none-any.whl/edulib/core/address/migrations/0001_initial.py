from django.db import (
    migrations,
    models,
)

import edulib.core.address.services.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')),
                ('place', models.UUIDField(blank=True, null=True, verbose_name='Населенный пункт')),
                ('street', models.UUIDField(blank=True, null=True, verbose_name='Улица')),
                ('house', models.UUIDField(blank=True, null=True, verbose_name='Дом')),
                ('house_num', models.CharField(blank=True, max_length=20, null=True, validators=[edulib.core.address.services.validators.HouseValidator()], verbose_name='Номер дома')),
                ('house_corps', models.CharField(blank=True, max_length=10, null=True, validators=[edulib.core.address.services.validators.BuildingValidator()], verbose_name='Корпус дома,')),
                ('flat', models.CharField(blank=True, max_length=50, null=True, verbose_name='Квартира')),
                ('zip_code', models.CharField(blank=True, max_length=6, null=True, verbose_name='Индекс')),
                ('full', models.CharField(blank=True, max_length=300, null=True, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
            },
        ),
    ]
