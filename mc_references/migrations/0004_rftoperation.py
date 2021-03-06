# Generated by Django 4.0.1 on 2022-02-03 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mc_references', '0003_rftcountry'),
    ]

    operations = [
        migrations.CreateModel(
            name='RftOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('o_code', models.CharField(db_index=True, max_length=2, verbose_name='Код операции')),
                ('o_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Наименование')),
                ('o_description', models.CharField(max_length=200, verbose_name='Полное наименование')),
                ('transp_type', models.SmallIntegerField(choices=[(0, 'Вагон'), (1, 'Контейнер')], verbose_name='Тип транспортного средства')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Операция',
                'verbose_name_plural': 'Операции',
                'db_table': 'RFT_OPERATION',
                'ordering': ['o_code'],
            },
        ),
    ]
