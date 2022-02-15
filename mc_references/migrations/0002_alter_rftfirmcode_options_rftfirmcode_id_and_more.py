# Generated by Django 4.0.1 on 2022-01-11 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mc_references', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rftfirmcode',
            options={'ordering': ['frc_code'], 'verbose_name': 'Фирма', 'verbose_name_plural': 'Фирмы'},
        ),
        migrations.AddField(
            model_name='rftfirmcode',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rftfirmcode',
            name='frc_code',
            field=models.CharField(db_index=True, max_length=10, verbose_name='Код ГВЦ'),
        ),
        migrations.AlterField(
            model_name='rftfirmcode',
            name='update_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата обновления'),
        ),
    ]
