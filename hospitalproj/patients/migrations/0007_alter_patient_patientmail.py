# Generated by Django 5.0.1 on 2024-02-17 14:51

import patients.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0006_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='PatientMail',
            field=models.EmailField(max_length=40),
        ),
    ]
