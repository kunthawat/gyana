# Generated by Django 3.2.11 on 2022-03-10 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0025_historicalfilter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filter',
            options={'ordering': ('created',)},
        ),
    ]
