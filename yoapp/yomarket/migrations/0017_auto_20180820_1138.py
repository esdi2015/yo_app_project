# Generated by Django 2.1 on 2018-08-20 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yomarket', '0016_qrcoupon_transaction_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcoupon',
            name='transaction_start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
