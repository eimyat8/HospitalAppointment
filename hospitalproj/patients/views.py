from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from .forms import UpdateForm, LoginForm, ScheduleForm, DateForm, DUpdateForm, searchForm, DoctorSignUpForm,PatientSignUpForm
from .models import Patient, Department, Doctor, Staff, Schedule, Appointment, History


# Create your views here.
def listform(request):
    pid = request.session.get('pid')
    if pid:
        pdata = Patient.objects.get(PatientID=pid)
        a_data = Appointment.objects.select_related('Patient').filter(Patient__PatientID=pid)
        h_data = History.objects.filter(Patient=pdata.PatientName)
        if a_data and h_data:
            print(a_data)
            return render(request, 'home.html', {'items': pdata, 'h_data': h_data, 'a_data': a_data})
        elif a_data:

            print("adata" , a_data)
            return render(request, 'home.html', {'items': pdata, 'a_data': a_data,'h_data':h_data})
        elif h_data:

            return render(request, 'home.html', {'items': pdata, 'h_data': h_data,'a_data':a_data})
        else:
            msg = "No data Here"
            return render(request, 'home.html', {'items': pdata,'msg':msg})


def doctorpage(request):
    did = request.session.get('did')
    if did:
        d_data = Doctor.objects.get(DoctorID=did)
        if request.method == "POST":
            dform = ScheduleForm(request.POST)
            if dform.is_valid():

                date = dform.cleaned_data['ScheduleDate']
                stime = dform.cleaned_data['ScheduleStartTime']
                etime = dform.cleaned_data['ScheduleEndTime']
                max_patients = dform.cleaned_data['MaxPatient']
                d_name = d_data.DoctorName
                doctor = get_object_or_404(Doctor, DoctorName=d_name)
                sch = Schedule.objects.create(Doctor=doctor, ScheduleDate=date, ScheduleStartTime=stime,
                                              ScheduleEndTime=etime,
                                              MaxPatient=max_patients)
                sch.save()

                return HttpResponseRedirect('/doctorsche/')
            else:
                pass
        else:
            dform = ScheduleForm()
            return render(request, 'doctor.html', {'form': dform, 'items': d_data})
        return render(request, 'doctor.html', {'items': d_data})


def staffpage(request):
    sid = request.session.get('sid')
    if sid:
        s_data = Staff.objects.get(id=sid)
        patient_count = Appointment.objects.filter(AppointDate=timezone.now().date()).count()
        doctor_count = Schedule.objects.filter(ScheduleDate=timezone.now().date()).count()
        count = (patient_count, doctor_count)
        return render(request, 'admindashb.html', {'items': s_data,'count':count})


def retreive_admin_patient_appointments(request):
    sid = request.session.get('sid')
    s_data = Staff.objects.get(id=sid)
    patient_count = Appointment.objects.filter(AppointDate=timezone.now().date()).count()
    doctor_count = Schedule.objects.filter(ScheduleDate=timezone.now().date()).count()
    count = (patient_count, doctor_count)
    appointment_table = Appointment.objects.filter(AppointDate=timezone.now().date())
    return render(request, 'admin_appointment_table.html',
                  {'appointment_table': appointment_table, 'count': count, 'items': s_data})


# admin dashboard show doctor's schedules
def retreive_admin_doctor_schedules(request):
    sid = request.session.get('sid')
    s_data = Staff.objects.get(id=sid)
    patient_count = Appointment.objects.filter(AppointDate=timezone.now().date()).count()
    doctor_count = Schedule.objects.filter(ScheduleDate=timezone.now().date()).count()
    count = (patient_count, doctor_count)
    result = Schedule.objects.filter(ScheduleDate=timezone.now().date())
    return render(request, 'admin_schedule_table.html', {'count': count, 'result': result, 'items': s_data})


def staffdoc(request):
    sid = request.session.get('sid')
    if sid:
        s_data = Staff.objects.get(id=sid)
        doctor_table = Doctor.objects.all()
        return render(request, 'admindoc.html', {'items': s_data, 'doctor_table': doctor_table})


def staffpatient(request):
    sid = request.session.get('sid')
    if sid:
        s_data = Staff.objects.get(id=sid)
        patient_table = Patient.objects.all()
        patient_name_query = request.GET.get('patient_name')
        message = ""
        if patient_name_query != '' and patient_name_query is not None:
            patient_table = patient_table.filter(PatientName__icontains=patient_name_query)

            message = "No of results found for " + "'" + str(patient_name_query) + "'" + " : " + str(
                patient_table.count())
        return render(request, 'adminpatient.html',
                      {'patient_table': patient_table, 'message': message, 'items': s_data})


def update_patient(request, id):
    sid = request.session.get('sid')
    if sid:
        s_data = Staff.objects.get(id=sid)
        data = Patient.objects.get(PatientID=id)
        form = UpdateForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            update_mail = form.cleaned_data['PatientMail']
            exist_mail = Patient.objects.filter(PatientMail=update_mail).exclude(PatientID=id)
            update_ph = form.cleaned_data['PatientPh']
            exist_ph = Patient.objects.filter(PatientPh=update_ph).exclude(PatientID=id)
            if exist_mail.exists():
                msg = "Email is already in use"
                return render(request, 'adminpedit.html', {'form': form, 'msg': msg, 'items': s_data})
            elif exist_ph.exists():
                msg = "Phone number is already in use"
                return render(request, 'adminpedit.html', {'form': form, 'msg': msg, 'items': s_data})
            else:
                form.save()
                return HttpResponseRedirect("/adminpatient/")
        else:
            form = UpdateForm(instance=data)
        return render(request, 'adminpedit.html', {'form': form, 'items': s_data})


def delete_patient(request, id):
    Patient.objects.get(PatientID=id).delete()
    return HttpResponseRedirect('/adminpatient/')


def update_doctor(request, id):
    data = Doctor.objects.get(DoctorID=id)
    form = DUpdateForm(request.POST, request.FILES, instance=data)
    if form.is_valid():
        update_mail = form.cleaned_data['DoctorMail']
        exist_mail = Doctor.objects.filter(DoctorMail=update_mail).exclude(DoctorID=id)
        update_ph = form.cleaned_data['DoctorPh']
        exist_ph = Doctor.objects.filter(DoctorPh=update_ph).exclude(DoctorID=id)
        if exist_mail.exists():
            msg = "Email is already in use"
            return render(request, 'dedit.html', {'form': form, 'msg': msg})
        elif exist_ph.exists():
            msg = "Phone number is already in use"
            return render(request, 'dedit.html', {'form': form, 'msg': msg})
        else:
            form.save()
            return HttpResponseRedirect("/admindoc/")
    else:
        form = DUpdateForm(instance=data)
        return render(request, 'admindedit.html', {'form': form})


def delete_doctor(request, id):
    Doctor.objects.get(DoctorID=id).delete()
    return HttpResponseRedirect('/admindoc/')


def staffschedule(request):
    sid = request.session.get('sid')
    if sid:
        s_data = Staff.objects.get(id=sid)
        schedule_table = Schedule.objects.all()
        doctor_name_query = request.GET.get('doctor_name')
        message = ""
        if doctor_name_query != '' and doctor_name_query is not None:
            schedule_table = schedule_table.filter(Doctor_id__DoctorName__icontains=doctor_name_query)
            print(schedule_table)
            print(schedule_table.query)
            message = "No of results found for " + "'" + str(doctor_name_query) + "'" + " : " + str(
                schedule_table.count())
        return render(request, 'adminschedule.html',
                      {'schedule_table': schedule_table, 'message': message, 'items': s_data})


def staffappoint(request):
    sid = request.session.get('sid')
    if sid:
        s_data = Staff.objects.get(id=sid)
        appointment_table = Appointment.objects.all()
        patient_name_query = request.GET.get('patient_name')
        doctor_name_query = request.GET.get('doctor_name')
        from_date_query = request.GET.get('from')
        to_date_query = request.GET.get('to')

        message = ""
        if (from_date_query == '' or from_date_query is None) or (to_date_query == '' or to_date_query is None):
            if (patient_name_query != '' and patient_name_query is not None) :
                appointment_table = Appointment.objects.filter(Patient_id__PatientName__icontains=patient_name_query)
                message = "Search results for " + "'" + str(patient_name_query) + "'" + " : " + str(appointment_table.count())
            if (doctor_name_query != '' and doctor_name_query is not None) :
                appointment_table = appointment_table.filter(Doctor_id__DoctorName__icontains=doctor_name_query)
                print("two ",appointment_table.query)
                message = "Search results for " + "'" + str(doctor_name_query) + "'" + " : " + str(appointment_table.count())
            if (patient_name_query != '' and patient_name_query is not None) and (doctor_name_query != '' and doctor_name_query is not None):
                appointment_table = Appointment.objects.filter(Patient_id__PatientName__icontains=patient_name_query, Doctor_id__DoctorName__icontains=doctor_name_query)
                print("three ",appointment_table.query)
                message = "Search results for patient name " + "'" + str(patient_name_query) + "'" +" and doctor name "+ "'" + str(doctor_name_query) + "'" + " : " + str(appointment_table.count())
        if (from_date_query != '' and from_date_query is not None) and (to_date_query != '' and to_date_query is not None):
            if ((patient_name_query != '' and patient_name_query is not None) and (doctor_name_query != '' and doctor_name_query is not None)):
                appointment_table = Appointment.objects.filter(AppointDate__range=(from_date_query, to_date_query),Patient_id__PatientName__icontains=patient_name_query,Doctor_id__DoctorName__icontains=doctor_name_query)
                message = "Search results for patient name " + "'" + str(patient_name_query) + "'" + ", Doctor name " + "'" + str(doctor_name_query) + "'" + " and appointment dates between" + "'" + str(from_date_query) + "'" +" and "+ "'" + str(to_date_query) + "'" + " : " + str(appointment_table.count())
                print("four ", appointment_table.query)
            elif (doctor_name_query != '' and doctor_name_query is not None) :
                appointment_table = appointment_table.filter(AppointDate__range=(from_date_query, to_date_query),Doctor_id__DoctorName__icontains=doctor_name_query)
                print("five ",appointment_table.query)
                message = "Search results for " + "'" + str(doctor_name_query) + "'" + " and appointment dates between" + "'" + str(from_date_query) + "'" +" and "+ "'" + str(to_date_query) + "'" + " : " + str(appointment_table.count())
            elif (patient_name_query != '' and patient_name_query is not None) :
                appointment_table = Appointment.objects.filter(AppointDate__range=(from_date_query, to_date_query),Patient_id__PatientName__icontains=patient_name_query)
                print("six ",appointment_table.query)
                message = "Search results for " + "'" + str(patient_name_query) + "'" + " and appointment dates between" + "'" + str(from_date_query) + "'" +" and "+ "'" + str(to_date_query) + "'" + " : " + str(appointment_table.count())
            else:
                appointment_table = Appointment.objects.filter(AppointDate__range=(from_date_query, to_date_query))
                message = "Search results for appointment dates between" + "'" + str(from_date_query) + "'" +" and "+ "'" + str(to_date_query) + "'" + " : " + str(appointment_table.count())
                print("seven ", appointment_table.query)
        return render(request, 'adminappoint.html', {'items':s_data,'appointment_table': appointment_table, 'message':message})



# def staffappoint(request):
#     sid = request.session.get('sid')
#     if sid:
#         s_data = Staff.objects.get(id=sid)
#         return render(request, 'adminappoint.html', {'items': s_data})


# Thazin Shane
def docsche(request):
    did = request.session.get('did')
    if did:
        d_data = Doctor.objects.get(DoctorID=did)
        d_name = d_data.DoctorName
        doctor = get_object_or_404(Doctor, DoctorName=d_name)
        data = Schedule.objects.filter(Doctor=doctor)
        if request.method == 'POST':
            cform = DateForm(request.POST)
            if cform.is_valid():
                fdate = cform.cleaned_data['startDate']
                edate = cform.cleaned_data['endDate']
                data = Schedule.objects.filter(Doctor=d_data, ScheduleDate__range=(fdate, edate))
                return render(request, 'docschedule.html', {'form': cform, 'schedule': data, 'items': d_data})
        else:
            data = Schedule.objects.filter(Doctor=d_data)
            cform = DateForm()
            return render(request, 'docschedule.html', {'form': cform, 'schedule': data, 'items': d_data})

        return render(request, 'docschedule.html', {'items': d_data})


def scheupdate(request, id):
    did = request.session.get('did')
    if did:
        d_data = Doctor.objects.get(DoctorID=did)
        data = Schedule.objects.get(ScheduleID=id)
        if request.method == 'POST':
            form = ScheduleForm(request.POST, instance=data)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/doctorsche/')
        else:
            form = ScheduleForm(instance=data)
            return render(request, 'dscheupdate.html', {'form': form, 'items': d_data})
    return render(request, 'docschedule.html', {'items': d_data})


def schedelete(request, id):
    Schedule.objects.get(ScheduleID=id).delete()
    return HttpResponseRedirect('/doctorsche/')


def docappoint(request):
    did = request.session.get('did')
    if did:
        d_data = Doctor.objects.get(DoctorID=did)
        if request.method == 'POST':
            cform = DateForm(request.POST)
            if cform.is_valid():
                fdate = cform.cleaned_data['startDate']
                edate = cform.cleaned_data['endDate']
                data = Appointment.objects.filter(Doctor=d_data, AppointDate__range=(fdate, edate))
                return render(request, 'docappoint.html', {'appointment': data, 'items': d_data, 'form': cform})
            else:
                data = Appointment.objects.filter(Doctor=d_data)
                cform = DateForm()
                return render(request, 'docappoint.html', {'appointment': data, 'items': d_data, 'form': cform})
        else:
            data = Appointment.objects.filter(Doctor=d_data)
            cform = DateForm()
            return render(request, 'docappoint.html', {'appointment': data, 'items': d_data, 'form': cform})
    else:

        cform = DateForm()
        return render(request, 'docappoint.html', {'form': cform})


def complete_appointment(request, id):
    if request.method == 'POST':
        # Retrieve the appointment object
        appointment = Appointment.objects.get(AppointmentID=id)

        # Create a record in the History table with the same data
        his = History.objects.create(
            Doctor=appointment.Doctor.DoctorName,
            Patient=appointment.Patient.PatientName,
            AppointDate=appointment.AppointDate,
            AppointStartTime=appointment.AppointStartTime,
            AppointEndTime=appointment.AppointEndTime,
            Token=appointment.Token,
            Status='Completed',
        )
        his.save()
        appointment.delete()
        return HttpResponseRedirect('/dochistory/')
    else:
        return redirect('/dochistory/')


def dochistory(request):
    did = request.session.get('did')
    if did:
        d_data = Doctor.objects.get(DoctorID=did)
        if request.method == 'POST':
            cform = DateForm(request.POST)
            if cform.is_valid():
                fdate = cform.cleaned_data['startDate']
                edate = cform.cleaned_data['endDate']
                data = History.objects.filter(Doctor=d_data, AppointDate__range=(fdate, edate))
                return render(request, 'dochistory.html', {'history': data, 'items': d_data, 'form': cform})
            else:
                data = History.objects.filter(Doctor=d_data)
                cform = DateForm()
                return render(request, 'dochistory.html', {'history': data, 'items': d_data, 'form': cform})
        else:
            data = History.objects.filter(Doctor=d_data)
            cform = DateForm()
            return render(request, 'dochistory.html', {'history': data, 'items': d_data, 'form': cform})
    else:

        cform = DateForm()
        return render(request, 'dochistory.html', {'form': cform})


def logout_view(request):
    logout(request)
    return redirect('dlogin')


def Plogout_view(request):
    logout(request)
    return redirect('/')


def Edit(request, id):
    data = Patient.objects.get(PatientID=id)
    form = UpdateForm(request.POST, request.FILES, instance=data)
    if form.is_valid():
        update_mail = form.cleaned_data['PatientMail']
        exist_mail = Patient.objects.filter(PatientMail=update_mail).exclude(PatientID=id)
        update_ph = form.cleaned_data['PatientPh']
        exist_ph = Patient.objects.filter(PatientPh=update_ph).exclude(PatientID=id)
        if exist_mail.exists():
            msg = "Email is already in use"
            return render(request, 'pedit.html', {'form': form, 'msg': msg})
        elif exist_ph.exists():
            msg = "Phone number is already in use"
            return render(request, 'pedit.html', {'form': form, 'msg': msg})
        else:
            form.save()
            return redirect("/list/")
    else:
        form = UpdateForm(instance=data)
    return render(request, 'pedit.html', {'form': form})


def viewdprofile(request):
    did = request.session.get('did')
    data = Doctor.objects.get(DoctorID=did)
    return render(request, 'dprofile.html', {'items': data})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['mail']
            pwd = form.cleaned_data['pwd']
            p_mail = Patient.objects.filter(PatientMail=mail, PatientPwd=pwd).first()
            if p_mail:
                request.session['pid'] = p_mail.PatientID
                return redirect('/list/')
            else:
                messages.error(request, 'Invalid mail or password!')
                return render(request, 'plogin.html', {'form': form})

    else:
        form = LoginForm()
    return render(request, 'plogin.html', {'form': form})


def doctorlogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['mail']
            pwd = form.cleaned_data['pwd']
            d_mail = Doctor.objects.filter(DoctorMail=mail, DoctorPwd=pwd).first()
            s_mail = Staff.objects.filter(AdminMail=mail, AdminPwd=pwd).first()
            if d_mail:
                request.session['did'] = d_mail.DoctorID
                return redirect('/docDashboard/')
            elif s_mail:
                request.session['sid'] = s_mail.id
                return redirect('/adminDashboard/')
            else:
                messages.error(request, 'Invalid mail or password!')
                return render(request, 'doctorlogin.html', {'form': form})

    else:
        form = LoginForm()
    return render(request, 'doctorlogin.html', {'form': form})


def schedule(request):
    data = Schedule.objects.all()
    if request.method == "POST":
        cform = DateForm(request.POST)
        if cform.is_valid():
            fdate = cform.cleaned_data['startDate']
            edate = cform.cleaned_data['endDate']
            data = Schedule.objects.filter(ScheduleDate__range=(fdate, edate))
            return render(request, 'docschedule.html', {'schedule': data, 'form': cform})
    else:
        cform = DateForm()
        return render(request, 'docschedule.html', {'schedule': data, 'form': cform})


def DocprofileEdit(request, id):
    data = Doctor.objects.get(DoctorID=id)
    form = DUpdateForm(request.POST, request.FILES, instance=data)
    if form.is_valid():
        update_mail = form.cleaned_data['DoctorMail']
        exist_mail = Doctor.objects.filter(DoctorMail=update_mail).exclude(DoctorID=id)
        update_ph = form.cleaned_data['DoctorPh']
        exist_ph = Doctor.objects.filter(DoctorPh=update_ph).exclude(DoctorID=id)
        if exist_mail.exists():
            msg = "Email is already in use"
            return render(request, 'dedit.html', {'form': form, 'msg': msg})
        elif exist_ph.exists():
            msg = "Phone number is already in use"
            return render(request, 'dedit.html', {'form': form, 'msg': msg})
        else:
            form.save()
            return HttpResponseRedirect("/dprofile/")
    else:
        form = DUpdateForm(instance=data)
        return render(request, 'dedit.html', {'form': form})


# Patients
def Departlist(request):
    data = Department.objects.all()
    return render(request, 'departmentaction.html', {'items': data})


def doctor_view(request, DepartID):
    data = Doctor.objects.filter(Department=DepartID)
    return render(request, 'searchDept.html', {'data': data})


def searchDoc(request):
    if request.method == 'POST':
        docname = request.POST['docname']
        doctors = Doctor.objects.filter(DoctorName__icontains=docname).order_by("DoctorName")
        if doctors:
            return render(request, 'pdocresult.html', {'doctors': doctors})
        else:
            message = f"No result found"
            return render(request, 'nosearchresult.html', {"message": message}, )
    else:
        data = Doctor.objects.all()
        return render(request, 'pdocresult.html', {'data': data})


def search_view(request):
    if request.method == 'POST':
        form = searchForm(request.POST)
        if form.is_valid():
            search_option = form.cleaned_data['searchby']
            if search_option == 'name':
                return redirect('searchDoc')
            elif search_option == 'department':
                return redirect('Departlist')
    else:
        form = searchForm()
    return render(request, 'stage1.html', {'form': form})


def appointment_view(request, DoctorID):
    data = Schedule.objects.filter(Doctor=DoctorID)
    if data:
        return render(request, 'stage3.html', {'schedule': data})
    else:
        return render(request,'nostage3.html',{'schedule':data})

# def tokenfun(request, id):
#     pid = request.session.get('pid')
#     if pid:
#         p_data = Patient.objects.get(PatientID=pid)
#         p_name = p_data.PatientName
#         patient = get_object_or_404(Patient, PatientName=p_name)
#         s_data = Schedule.objects.get(ScheduleID=id)
#         s_doc = s_data.Doctor
#         pcount = s_data.MaxPatient
#
#         a_data = Appointment.objects.filter(Doctor=s_doc)
#         old_token = 0
#         if a_data.exists():
#             old_token = a_data.order_by('-Token')[0].Token
#
#         if pcount > 0:
#             new_token = int(old_token) + 1
#             new_appointment = Appointment.objects.create(
#                 Doctor=s_doc,
#                 Patient=patient,
#                 Status="Scheduled",
#                 AppointDate=s_data.ScheduleDate,
#                 AppointStartTime=s_data.ScheduleStartTime,
#                 AppointEndTime=s_data.ScheduleEndTime,
#                 Token=str(new_token)
#             )
#             new_appointment.save()
#             s_data.MaxPatient -= 1
#             s_data.save()
#             return render(request, 'stage4.html', {'token': new_token})
#         else:
#             msg = "Doctor's schedule is full"
#         return render(request, 'stage4.html', {'msg': msg})


def tokenfun(request, id):
    pid = request.session.get('pid')
    if pid:
        p_data = Patient.objects.get(PatientID=pid)
        p_name = p_data.PatientName
        patient = get_object_or_404(Patient, PatientName=p_name)
        s_data = get_object_or_404(Schedule, ScheduleID=id)
        s_doc = s_data.Doctor
        pcount = s_data.MaxPatient

        a_data = Appointment.objects.filter(Doctor=s_doc)
        old_token = 0
        if a_data.exists():
            old_token = int(a_data.order_by('-Token')[0].Token)

        if pcount > 0:
            new_token = old_token + 1
            new_appointment = Appointment.objects.create(
                Doctor=s_doc,
                Patient=patient,
                Status="Scheduled",
                AppointDate=s_data.ScheduleDate,
                AppointStartTime=s_data.ScheduleStartTime,
                AppointEndTime=s_data.ScheduleEndTime,
                Token=str(new_token)
            )
            new_appointment.save()
            s_data.MaxPatient -= 1
            s_data.save()
            return render(request, 'stage4.html', {'token': new_token})
        else:
            msg = "Doctor's schedule is full"
    else:
        msg = "Patient ID not found in session"

    return render(request, 'stage4.html', {'msg': msg})


def cancel_appointment(request, id):
    if request.method == 'POST':
        # Retrieve the appointment object
        appointment = Appointment.objects.get(AppointmentID=id)
        s_data = Schedule.objects.get(Doctor=appointment.Doctor, ScheduleDate=appointment.AppointDate)
        s_data.MaxPatient += 1
        s_data.save()

        appointment.delete()
        return HttpResponseRedirect('/list/')
    else:
        return redirect('/list/')

def deleteHistory(request,id):
    History.objects.get(HistoryID=id).delete()
    return HttpResponseRedirect('/dochistory/')

#Sign Up
def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():

            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('/dlogin/')  # Redirect to login page after successful signup
    else:
        form = DoctorSignUpForm()
    return render(request, 'dsignup.html', {'form': form})

def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Your account has been created successfully!')
            return redirect('/login/')  # Redirect to login page after successful signup
    else:
        form = PatientSignUpForm()
    return render(request, 'psignup.html', {'form': form})