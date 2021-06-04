# Generated by Django 3.2 on 2021-06-03 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0005_alter_widget_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widget',
            name='kind',
            field=models.CharField(choices=[('table', 'Table'), ('column2d', 'Column'), ('line', 'Line'), ('pie2d', 'Pie')], default='column2d', max_length=32),
        ),
    ]
