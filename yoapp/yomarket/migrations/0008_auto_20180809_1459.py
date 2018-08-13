# Generated by Django 2.0.7 on 2018-08-09 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yomarket', '0007_auto_20180808_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='QRcoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=36, unique=True)),
                ('short_uuid', models.CharField(max_length=8, unique=True)),
                ('available', models.BooleanField(default=True)),
                ('expiry_date', models.DateTimeField()),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('offer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offer', to='yomarket.Offer')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='shop',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shops_manager', to=settings.AUTH_USER_MODEL),
        ),
    ]