# Generated by Django 5.0.6 on 2024-07-22 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_hall_size_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hall',
            name='price',
            field=models.BigIntegerField(),
        ),
    ]
