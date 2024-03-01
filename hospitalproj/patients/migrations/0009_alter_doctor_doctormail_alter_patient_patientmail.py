# Generated by Django 5.0.1 on 2024-02-19 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0008_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='DoctorMail',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='PatientMail',
            field=models.EmailField(max_length=40, unique=True),
        ),
    ]