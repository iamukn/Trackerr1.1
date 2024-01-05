# Generated by Django 4.2.7 on 2024-01-05 00:22

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="YourModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "array_field",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100), size=4
                    ),
                ),
            ],
        ),
    ]
