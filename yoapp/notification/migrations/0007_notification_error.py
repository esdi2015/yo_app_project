# Generated by Django 2.0.7 on 2018-08-30 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0006_notification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='error',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]