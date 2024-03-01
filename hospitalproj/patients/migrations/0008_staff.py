# Generated by Django 5.0.1 on 2024-02-18 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0007_alter_patient_patientmail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AdminName', models.CharField(max_length=20)),
                ('AdminMail', models.EmailField(max_length=20)),
                ('AdminPwd', models.CharField(max_length=20)),
                ('AdminImg', models.ImageField(default='a.png', upload_to='uploads')),
            ],
        ),
    ]
