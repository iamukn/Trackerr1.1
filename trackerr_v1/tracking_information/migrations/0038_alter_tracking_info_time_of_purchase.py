# Generated by Django 4.2.10 on 2024-12-09 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_information', '0037_alter_tracking_info_time_of_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracking_info',
            name='time_of_purchase',
            field=models.CharField(default='18:55hrs'),
        ),
    ]
