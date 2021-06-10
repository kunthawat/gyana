# Generated by Django 3.2 on 2021-06-10 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0014_auto_20210610_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='date_value',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='filter',
            name='datetime_value',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='filter',
            name='type',
            field=models.CharField(choices=[('INTEGER', 'Integer'), ('FLOAT', 'Float'), ('STRING', 'String'), ('BOOL', 'Bool'), ('TIME', 'Time'), ('DATE', 'Date'), ('DATETIME', 'Datetime')], max_length=8),
        ),
    ]
