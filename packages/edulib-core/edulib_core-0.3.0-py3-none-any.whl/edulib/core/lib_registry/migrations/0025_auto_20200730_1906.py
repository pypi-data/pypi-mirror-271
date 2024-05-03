"""Миграции."""
# flake8: noqa
import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('lib_registry', '0024_replace_writeoff_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibExchangeFund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f')),
                ('previous_lib_reg_entry_id', models.IntegerField(verbose_name='\u0418\u043d\u0432. \u2116 \u043a\u043e\u043f\u0438\u0440\u0443\u0435\u043c\u043e\u0439 \u043a\u0430\u0440\u0442\u043e\u0447\u043a\u0438 \u0443\u0447\u0435\u0442\u0430 \u044d\u043a\u0437\u0435\u043c\u043b\u044f\u0440\u0430')),
                ('future_lib_reg_entry_id', models.IntegerField(blank=True, null=True, verbose_name='\u0418\u043d\u0432. \u2116 \u043a\u0430\u0440\u0442\u043e\u0447\u043a\u0438 \u0443\u0447\u0435\u0442\u0430 \u044d\u043a\u0437\u0435\u043c\u043b\u044f\u0440\u0430 \u0432 \u0441\u043b\u0443\u0447\u0430\u0435 \u043f\u0435\u0440\u0435\u0434\u0430\u0447\u0438 \u0432 \u0448\u043a\u043e\u043b\u0443-\u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044c')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='\u0421\u0440\u043e\u043a c')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='\u0421\u0440\u043e\u043a \u043f\u043e')),
                ('note', models.CharField(blank=True, max_length=256, null=True, verbose_name='\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u0435')),
                ('send_to_fund', models.BooleanField(default=False, verbose_name='\u0412\u044b\u0434\u0430\u043d\u043e \u0438\u0437 \u0444\u043e\u043d\u0434\u0430 \u0432 \u0448\u043a\u043e\u043b\u0443-\u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044c')),
                ('received_from_fund', models.BooleanField(default=True, verbose_name='\u041f\u043e\u043b\u0443\u0447\u0435\u043d\u043e \u043e\u0442 \u0448\u043a\u043e\u043b\u044b-\u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f \u043e\u0431\u0440\u0430\u0442\u043d\u043e \u0432 \u0444\u043e\u043d\u0434')),
            ],
            options={
                'db_table': 'lib_exchange_fund',
            },
        ),
        migrations.AddField(
            model_name='libregistryentry',
            name='all_in_fund',
            field=models.BooleanField(default=False, verbose_name='\u041a\u0430\u0440\u0442\u043e\u0447\u043a\u0430 \u0441\u043e \u0432\u0441\u0435\u043c\u0438 \u044d\u043a\u0437\u0435\u043c\u043f\u043b\u044f\u0440\u0430\u043c\u0438 \u043f\u0435\u0440\u0435\u0434\u0430\u043d\u0430 \u0432 \u0444\u043e\u043d\u0434'),
        ),
        migrations.AddField(
            model_name='libregistryentry',
            name='take_from_fund',
            field=models.BooleanField(default=False, verbose_name='\u041f\u043e\u043b\u0443\u0447\u0435\u043d\u043e \u0438\u0437 \u0444\u043e\u043d\u0434\u0430'),
        ),
        migrations.AddField(
            model_name='libexchangefund',
            name='lib_reg_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lib_registry.LibRegistryEntry', verbose_name='\u041a\u0430\u0440\u0442\u043e\u0447\u043a\u0430 \u0443\u0447\u0435\u0442\u0430 \u044d\u043a\u0437\u0435\u043c\u043f\u043b\u044f\u0440\u0430'),
        ),
        migrations.AddField(
            model_name='libexchangefund',
            name='school',
            field=models.BigIntegerField(verbose_name='\u0428\u043a\u043e\u043b\u0430'),
        ),
        migrations.AddField(
            model_name='libexchangefund',
            name='teacher',
            field=models.BigIntegerField(verbose_name='\u0424\u0418\u041e \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u0430'),
        ),
    ]
