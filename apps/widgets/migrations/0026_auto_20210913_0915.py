# Generated by Django 3.2.7 on 2021-09-13 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("widgets", "0025_alter_widget_kind"),
    ]

    operations = [
        migrations.RenameField(
            model_name="widget",
            old_name="label",
            new_name="dimension",
        ),
        migrations.RemoveField(
            model_name="widget",
            name="value",
        ),
        migrations.AlterField(
            model_name="widget",
            name="sort_by",
            field=models.CharField(
                choices=[("dimension", "Dimension"), ("value", "Value")],
                default="dimension",
                max_length=12,
            ),
        ),
        migrations.RunSQL(
            """
        UPDATE widgets_widget
        SET sort_by=CASE 
                        WHEN sort_by='label' THEN 'dimension' 
                        ELSE 'metric'
                    END
        """,
            reverse_sql="""
        UPDATE widgets_widget
        SET sort_by=CASE 
                        WHEN sort_by='dimension' THEN 'label' 
                        ELSE 'value'
                    END
        """,
        ),
    ]
