# Generated by Django 3.2.7 on 2021-12-17 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0042_auto_20211216_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='widget',
            name='rounding_decimal',
            field=models.IntegerField(default=2),
        ),
    ]
