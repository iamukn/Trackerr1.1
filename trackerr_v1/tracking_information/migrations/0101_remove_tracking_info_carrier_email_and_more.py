# Generated by Django 4.2.10 on 2024-04-13 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("logistics", "0001_initial"),
        ("tracking_information", "0100_tracking_info_destination_lat_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tracking_info",
            name="carrier_email",
        ),
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
        migrations.AlterField(
            model_name="tracking_info",
            name="owner",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
