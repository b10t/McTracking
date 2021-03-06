# Generated by Django 4.0.1 on 2022-02-18 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mc_references', '0018_alter_rftrwctype_rt_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='RftRwcModel',
            fields=[
                ('rm_code', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Код модели вагона')),
                ('rm_osob', models.CharField(max_length=100, verbose_name='Наименование модели вагона')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Модель вагона',
                'verbose_name_plural': 'Модели вагонов',
                'db_table': 'RFT_RWC_MODEL',
                'ordering': ['rm_code'],
            },
        ),
    ]
