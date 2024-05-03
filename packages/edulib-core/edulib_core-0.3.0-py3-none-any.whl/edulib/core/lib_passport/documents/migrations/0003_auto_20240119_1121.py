from django.db import (
    migrations,
    models,
)

import edulib.core.base.files


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20180420_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libpassportdocuments',
            name='document',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=edulib.core.base.files.upload_file_handler, verbose_name='Файл'),
        ),
    ]
