# Generated by Django 3.2.7 on 2021-09-13 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0013_auto_20210822_0024'),
        ('nodes', '0010_alter_node_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='input_table',
            field=models.ForeignKey(help_text='Select a data source', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tables.table'),
        ),
    ]
