from django.db import (
    migrations,
    models,
)

import edulib.core.base.files


class Migration(migrations.Migration):

    dependencies = [
        ('lib_registry', '0033_auto_20220704_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libregistryentry',
            name='cover',
            field=models.ImageField(blank=True, max_length=3072, null=True, upload_to=edulib.core.base.files.upload_file_handler, verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='filename',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=edulib.core.base.files.upload_named_handler, verbose_name='Файл'),
        ),
    ]
