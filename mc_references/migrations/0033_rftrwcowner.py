# Generated by Django 4.0.1 on 2022-03-04 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mc_references', '0032_alter_rftrwcgroup_rwc_parent_group_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RftRwcOwner',
            fields=[
                ('owner_no', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Код собственника')),
                ('owner_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Наименование собственника')),
                ('parent_owner_no', models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='Код род. группы')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Группа собственника вагона',
                'verbose_name_plural': 'Группы собственников вагонов',
                'db_table': 'RFT_RWC_OWNER',
                'ordering': ['owner_no'],
            },
        ),
    ]
