from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('',TemplateView.as_view(template_name='index.html')),
    path('login/',views.login,name='login'),
    path('list/', views.listform, name='list'),
    path('edit/<int:id>', views.Edit, name='Edit'),
    path('index/', TemplateView.as_view(template_name='index.html')),
    path('depart/', views.Departlist, name='depart'),
    # Doctor
    path('dlogin/', views.doctorlogin, name ='dlogin'),
    path('docDashboard/', views.doctorpage, name='doctor'),
    path('doctorsche/',views.docsche,name="doctorsche"),
    path('docappoint/', views.docappoint, name='docappoint'),
    path('dochistory/', views.dochistory, name='dochistory'),
    path('dhisdel/<int:id>',views.deleteHistory,name='dhisdel'),
    path('dscheupdate/<int:id>', views.scheupdate, name='dscheupdate'),
    path('dschedelete/<int:id>/', views.schedelete, name='dschedelete'),
    path('dprofile/', views.viewdprofile, name='dprofile'),
    path('dedit/<int:id>',views.DocprofileEdit, name='dedit'),
    path('doctorsche/', views.schedule, name='doctorsche'),
    path('complete_appointment/<int:id>/', views.complete_appointment, name='complete_appointment'),
    path('logoutcd/', views.logout_view, name='logout'),
    # admin
    path('retreive_admin_patient_appointments/', views.retreive_admin_patient_appointments,name='retreive_admin_patient_appointments'),
    path('retreive_admin_doctor_schedules/', views.retreive_admin_doctor_schedules,name='retreive_admin_doctor_schedules'),
    path('adminDashboard/', views.staffpage, name= 'adminDashboard'),
    path('admindoc/', views.staffdoc, name='admindoc'),
    path('adminappoint/', views.staffappoint, name= 'adminappoint'),
    path('adminsche/', views.staffschedule, name= 'adminsche'),
    path('adminpatient/', views.staffpatient, name= 'adminpatient'),
    path('update_doctor/<int:id>/', views.update_doctor, name='update_doctor'),
    path('delete_doctor/<int:id>/', views.delete_doctor, name='delete_doctor'),
    path('update_patient/<int:id>/',views.update_patient, name='update_patient'),
    path('delete_patient/<int:id>/', views.delete_patient, name='delete_patient'),
    #patients
    path('search/', views.search_view, name="search_view"),
    path('searchdoc/',views.searchDoc,name='searchDoc'),
    path('Departlist/',views.Departlist,name='Departlist'),
    path('doctors/<int:DepartID>/',views.doctor_view,name='doctor_view'),
    path('appointment/<int:DoctorID>/',views.appointment_view,name='appointment_view'),
    path('logoutp/', views.Plogout_view, name='logoutp'),
    path('tokenfun/<int:id>',views.tokenfun, name='tokenfun'),
    path('list/<int:id>/',views.cancel_appointment,name='list'),

    #SignUp
    path('psignup/', views.patient_signup, name='psignup'),
    path('dsignup/', views.doctor_signup, name='dsignup'),



]