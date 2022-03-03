# Generated by Django 4.0.1 on 2022-03-03 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mc_references', '0022_alter_rftconttype_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RftRepairType',
            fields=[
                ('rpt_code', models.CharField(max_length=2, primary_key=True, serialize=False, verbose_name='Код типа ремонта')),
                ('rpt_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Наименование типа ремонта')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Тип ремонта',
                'verbose_name_plural': 'Типы ремонтов',
                'db_table': 'RFT_REPAIR_TYPE',
                'ordering': ['rpt_code'],
            },
        ),
    ]