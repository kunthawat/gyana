# Generated by Django 3.2.7 on 2021-12-16 11:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0041_widget_show_summary_row'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='widget',
            options={},
        ),
        migrations.AddField(
            model_name='widget',
            name='background_color',
            field=models.CharField(max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='widget',
            name='font_color',
            field=models.CharField(max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='widget',
            name='font_size',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='widget',
            name='palette_colors',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='#5D62B5', max_length=7), null=True, size=10),
        ),
        migrations.AddField(
            model_name='widget',
            name='show_tooltips',
            field=models.BooleanField(null=True),
        ),
    ]
