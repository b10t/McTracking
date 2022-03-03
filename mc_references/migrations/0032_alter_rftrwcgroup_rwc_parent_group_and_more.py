# Generated by Django 4.0.1 on 2022-03-03 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mc_references', '0031_alter_rftrwcgroup_rwc_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rftrwcgroup',
            name='rwc_parent_group',
            field=models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='Код род. группы'),
        ),
        migrations.AlterField(
            model_name='rftrwcgroup',
            name='rwc_top_group',
            field=models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='Код группы верхнего уровня'),
        ),
    ]