# Generated by Django 2.0.7 on 2018-08-27 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_auto_20180823_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification_settings',
            name='last_run_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
