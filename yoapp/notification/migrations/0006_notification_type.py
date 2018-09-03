# Generated by Django 2.0.7 on 2018-08-28 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0005_subscription_notification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('email', 'Email-msg'), ('push', 'Push-msg')], default='email', max_length=5),
        ),
    ]