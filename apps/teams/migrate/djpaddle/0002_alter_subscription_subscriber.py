# Generated by Django 3.2.7 on 2021-11-11 01:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_initial'),
        ('djpaddle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='subscriber',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='teams.team'),
        ),
    ]
