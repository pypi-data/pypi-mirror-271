from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('lib_registry', '0034_auto_20240119_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libsummarybook',
            name='school',
            field=models.BigIntegerField(verbose_name='Организация'),
        ),
        migrations.RenameField(
            model_name='libsummarybook',
            old_name='school',
            new_name='school_id',
        ),
        migrations.AlterField(
            model_name='libsummarybookdisposal',
            name='school',
            field=models.BigIntegerField(verbose_name='Организация'),
        ),
        migrations.RenameField(
            model_name='libsummarybookdisposal',
            old_name='school',
            new_name='school_id',
        ),
        migrations.AlterField(
            model_name='libexchangefund',
            name='school',
            field=models.BigIntegerField(verbose_name='Школа'),
        ),
        migrations.RenameField(
            model_name='libexchangefund',
            old_name='school',
            new_name='school_id',
        ),
        migrations.AlterField(
            model_name='libsummarybookcalculated',
            name='school',
            field=models.BigIntegerField(verbose_name='Школа'),
        ),
        migrations.RenameField(
            model_name='libsummarybookcalculated',
            old_name='school',
            new_name='school_id',
        ),
    ]
