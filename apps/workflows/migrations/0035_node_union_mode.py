# Generated by Django 3.2 on 2021-07-08 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0034_node_select_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='union_mode',
            field=models.CharField(choices=[('keep', 'keep'), ('exclude', 'exclude')], default='except', max_length=8),
        ),
    ]
