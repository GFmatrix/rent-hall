# Generated by Django 5.0.6 on 2024-07-22 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_hall_google_map'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hall',
            name='google_map',
            field=models.URLField(blank=True),
        ),
    ]
