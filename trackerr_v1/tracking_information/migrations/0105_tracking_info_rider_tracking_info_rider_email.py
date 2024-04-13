# Generated by Django 4.2.10 on 2024-04-13 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("logistics", "0001_initial"),
        ("tracking_information", "0104_remove_tracking_info_rider_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tracking_info",
            name="rider",
            field=models.OneToOneField(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="logistics.logistics_partner",
            ),
        ),
        migrations.AddField(
            model_name="tracking_info",
            name="rider_email",
            field=models.EmailField(
                blank=True, default=None, max_length=255, null=True
            ),
        ),
    ]
