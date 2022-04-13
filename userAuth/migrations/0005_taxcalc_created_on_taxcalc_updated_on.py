# Generated by Django 4.0.4 on 2022-04-12 16:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0004_taxcalc_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxcalc',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 4, 12, 16, 56, 33, 281009, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxcalc',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
