# Generated by Django 3.2.9 on 2021-11-19 20:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0009_auto_20211120_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 20, 7, 11, 506197, tzinfo=utc)),
        ),
    ]