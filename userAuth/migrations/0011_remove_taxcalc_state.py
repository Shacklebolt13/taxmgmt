# Generated by Django 4.0.4 on 2022-04-14 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0010_taxcalc_pan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taxcalc',
            name='state',
        ),
    ]
