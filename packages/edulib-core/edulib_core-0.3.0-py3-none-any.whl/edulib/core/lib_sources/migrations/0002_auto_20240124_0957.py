from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('lib_sources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarysource',
            name='school',
            field=models.BigIntegerField(verbose_name='организация'),
        ),
        migrations.RenameField(
            model_name='librarysource',
            old_name='school',
            new_name='school_id',
        ),
    ]
