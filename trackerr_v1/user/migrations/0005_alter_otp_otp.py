# Generated by Django 4.2.10 on 2024-11-18 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='otp',
            field=models.CharField(blank=True, default=None, max_length=8, null=True, verbose_name='otp'),
        ),
    ]