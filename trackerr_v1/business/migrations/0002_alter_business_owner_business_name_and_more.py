# Generated by Django 4.2.10 on 2024-06-30 10:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("business", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="business_owner",
            name="business_name",
            field=models.CharField(
                max_length=500, unique=True, verbose_name="business name"
            ),
        ),
        migrations.AlterField(
            model_name="business_owner",
            name="service",
            field=models.CharField(
                default="parcel delivery", max_length=200, verbose_name="services"
            ),
        ),
    ]
