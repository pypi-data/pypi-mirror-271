from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('lib_sources', '0002_auto_20240124_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarysource',
            name='name',
            field=models.TextField(verbose_name='Источник поступления'),
        ),
        migrations.AlterField(
            model_name='librarysource',
            name='school_id',
            field=models.BigIntegerField(verbose_name='Организация'),
        ),
    ]