# Generated by Django 4.0.1 on 2022-02-18 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mc_references', '0020_alter_rftrwcmodel_rm_osob'),
    ]

    operations = [
        migrations.CreateModel(
            name='RftContType',
            fields=[
                ('rt_code', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Код типа контейнера')),
                ('rt_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Наименование типа контейнера')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Тип контейнера',
                'verbose_name_plural': 'Типы контейнеров',
                'db_table': 'RFT_CONT_TYPE',
                'ordering': ['rt_code'],
            },
        ),
    ]
