# Generated by Django 4.2.7 on 2024-01-18 15:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("serializer", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="color",
            field=models.CharField(),
        ),
    ]
