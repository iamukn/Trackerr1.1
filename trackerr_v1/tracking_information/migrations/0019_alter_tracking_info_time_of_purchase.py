# Generated by Django 4.2.10 on 2024-06-30 10:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracking_information", "0018_alter_tracking_info_time_of_purchase"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tracking_info",
            name="time_of_purchase",
            field=models.CharField(default="10:16hrs"),
        ),
    ]
