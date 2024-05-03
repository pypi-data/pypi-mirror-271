from django.db import (
    migrations,
    models,
)

import edulib.core.base.files


class Migration(migrations.Migration):

    dependencies = [
        ('library_scanned_copy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scannedcopy',
            name='filename',
            field=models.FileField(max_length=255, upload_to=edulib.core.base.files.upload_named_handler, verbose_name='Файл'),
        ),
    ]
