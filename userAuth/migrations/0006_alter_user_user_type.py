# Generated by Django 4.0.4 on 2022-04-13 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0005_taxcalc_created_on_taxcalc_updated_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'TaxPayer'), (2, 'TaxAccountant'), (3, 'Admin')], default=1, editable=False),
        ),
    ]
