# Generated by Django 4.0.1 on 2022-02-15 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mc_references', '0008_rftrlwdep'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rftrailway',
            name='cntr_ide',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mc_references.rftcountry', verbose_name='Страна'),
        ),
    ]
