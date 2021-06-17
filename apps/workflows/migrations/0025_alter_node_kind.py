# Generated by Django 3.2 on 2021-06-17 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workflows", "0024_auto_20210615_1427"),
    ]

    operations = [
        migrations.AlterField(
            model_name="node",
            name="kind",
            field=models.CharField(
                choices=[
                    ("input", "Input"),
                    ("output", "Output"),
                    ("select", "Select"),
                    ("join", "Join"),
                    ("aggregation", "Aggregation"),
                    ("union", "Union"),
                    ("sort", "Sort"),
                    ("limit", "Limit"),
                    ("filter", "Filter"),
                    ("edit", "Edit"),
                    ("add", "Add"),
                    ("rename", "Rename"),
                    ("text", "Text"),
                    ("distinct", "Distinct"),
                ],
                max_length=16,
            ),
        ),
    ]
