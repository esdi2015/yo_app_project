# Generated by Django 2.0.7 on 2018-07-31 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_region'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ('region_name',), 'verbose_name': 'region', 'verbose_name_plural': 'regions'},
        ),
    ]
