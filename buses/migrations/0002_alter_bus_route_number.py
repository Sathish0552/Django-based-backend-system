# Generated by Django 4.2.19 on 2025-02-17 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='route_number',
            field=models.CharField(max_length=20),
        ),
    ]
