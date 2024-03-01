from django.contrib import admin
from .models import Patient,Department,Doctor,Staff,Appointment,Schedule,History

# Register your models here.
admin.site.register(Patient)
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Staff)
admin.site.register(Appointment)
admin.site.register(Schedule)
admin.site.register(History)