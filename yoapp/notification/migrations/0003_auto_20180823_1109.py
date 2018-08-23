# Generated by Django 2.0.7 on 2018-08-23 11:09

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('yomarket', '0023_auto_20180822_1035'),
        ('notification', '0002_auto_20180822_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification_settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(blank=True, max_length=150, null=True)),
                ('last_run_time', models.DateTimeField(blank=True, default=datetime.datetime(2018, 8, 23, 11, 9, 23, 882869, tzinfo=utc), null=True)),
            ],
            options={
                'verbose_name': 'notif_settings',
            },
        ),
        migrations.AddField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='is_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='yomarket.Offer'),
        ),
    ]
