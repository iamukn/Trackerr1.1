# Generated by Django 4.2.10 on 2024-12-16 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_alter_business_owner_business_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='business_owner',
            name='latitude',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='latitude'),
        ),
        migrations.AddField(
            model_name='business_owner',
            name='longitude',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='longitude'),
        ),
    ]
