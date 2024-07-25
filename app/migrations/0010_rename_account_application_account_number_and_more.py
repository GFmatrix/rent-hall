# Generated by Django 5.0.6 on 2024-07-22 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_hall_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='account',
            new_name='account_number',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='phone',
            new_name='phone_number',
        ),
        migrations.AlterField(
            model_name='application',
            name='application_id',
            field=models.CharField(blank=True, max_length=6, unique=True),
        ),
    ]
