# Generated by Django 4.0.4 on 2022-04-13 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0008_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxcalc',
            name='due_on',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]