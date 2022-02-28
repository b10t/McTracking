# Generated by Django 4.0.1 on 2022-02-18 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mc_references', '0013_alter_rftstation_cntr_ide_alter_rftstation_rlw_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='RftDepo',
            fields=[
                ('dp_code', models.CharField(max_length=4, primary_key=True, serialize=False, verbose_name='Код депо')),
                ('dp_name', models.CharField(max_length=100, verbose_name='Наименование депо')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Депо',
                'verbose_name_plural': 'Депо',
                'db_table': 'RFT_DEPO',
                'ordering': ['dp_code'],
            },
        ),
    ]