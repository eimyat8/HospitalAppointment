# Generated by Django 5.0.1 on 2024-02-12 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_alter_patient_patientimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='PatientImg',
            field=models.ImageField(default='a.png', upload_to='uploads'),
        ),
    ]
