# Generated by Django 4.0.1 on 2022-02-18 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mc_references', '0015_rename_update_date_rftdepo_dp_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rftdepo',
            name='dp_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Наименование депо'),
        ),
    ]
