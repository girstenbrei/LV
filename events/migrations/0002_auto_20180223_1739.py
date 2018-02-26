# Generated by Django 2.0.2 on 2018-02-23 16:39

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='signup_from',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 23, 16, 39, 7, 752862, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='signup_to',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 23, 16, 39, 17, 80655, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
