from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Patient(models.Model):
    PatientID = models.AutoField(primary_key=True)
    PatientImg = models.ImageField(upload_to='uploads',default='a.png')
    PatientName = models.CharField(max_length=40)
    PatientMail = models.EmailField(max_length=40)
    PatientPh =models.CharField(max_length=30)
    PatientDob = models.DateField()
    PatientAddr = models.CharField(max_length=100)
    PatientPwd = models.CharField(max_length=30)

    def __str__(self):
        return self.PatientName


class Department(models.Model):
    DepartID = models.AutoField(primary_key=True)
    DepartImg = models.ImageField(upload_to='uploads')
    DepartName = models.CharField(max_length=50)

    def __str__(self):
        return self.DepartName

class Doctor(models.Model):
    DoctorID = models.AutoField(primary_key= True)
    DoctorImg = models.ImageField(upload_to='uploads',default='a.png')
    DoctorName = models.CharField(max_length=50)
    DoctorMail =models.EmailField(max_length=50)
    DoctorPwd = models.CharField(max_length=50)
    DoctorPh = models.CharField(max_length=50)
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return self.DoctorName

class Staff(models.Model):
    AdminName= models.CharField(max_length=20)
    AdminMail = models.EmailField(max_length=20)
    AdminPwd = models.CharField(max_length=20)
    AdminImg = models.ImageField(upload_to='uploads',default='a.png')

    def __str__(self):
        return self.AdminName

class Appointment(models.Model):
    AppointmentID = models.AutoField(primary_key=True)
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    AppointDate = models.DateField()
    AppointStartTime = models.TimeField()
    AppointEndTime = models.TimeField()
    Token = models.CharField(max_length=255)
    Status = models.CharField(max_length=10)

    def __int__(self):
        return self.AppointmentID


class History(models.Model):
    HistoryID = models.AutoField(primary_key=True)
    Doctor = models.CharField(max_length=30)
    Patient = models.CharField(max_length=30)
    AppointDate = models.DateField(default="")
    AppointStartTime = models.TimeField()
    AppointEndTime = models.TimeField()
    Token = models.CharField(max_length=255)
    Status = models.CharField(max_length=10)

    def __str__(self):
        return self.Doctor

class Schedule(models.Model):
    ScheduleID = models.AutoField(primary_key=True)
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    ScheduleDate = models.DateField(null=True, blank=True)
    ScheduleStartTime = models.TimeField()
    ScheduleEndTime = models.TimeField()
    MaxPatient = models.PositiveIntegerField()

    def __int__(self):
        return self.ScheduleID
