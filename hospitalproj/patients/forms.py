from django.core.exceptions import ValidationError

from .models import Patient,Schedule,Appointment,Doctor,Department
from django import forms
from django.utils.translation import gettext_lazy as _


class UpdateForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields =['PatientImg','PatientName','PatientMail','PatientPh','PatientDob','PatientAddr','PatientPwd']
        labels={
            'PatientImg':_('Profile Photo',),
            'PatientName': _("Name"),
            'PatientMail':_('Email'),
            'PatientPh':_('Phone No.'),
            'PatientDob': _('Date of Birth'),
            'PatientAddr':_('Address'),
            'PatientPwd':_('Password')
        }
        widgets={
            'PatientMail': forms.EmailInput(attrs={'type':'email', 'placeholder':'Enter your email'}),
            'PatientDob': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd'}),
            'PatientName': forms.TextInput(attrs={ 'placeholder': 'Enter your name'}),
            'PatientAddr': forms.Textarea(attrs={'placeholder': 'Enter your address'}),
            'PatientPwd': forms.TextInput(attrs={'placeholder': 'Enter your password'}),
        }

class DUpdateForm(forms.ModelForm):
    class Meta:
        model= Doctor
        fields=['DoctorImg','DoctorName','DoctorMail','DoctorPwd','DoctorPh','Department']
        labels = {
            'DoctorImg': _('Photo', ),
            'DoctorName': _("Name"),
            'DoctorMail': _('Email'),
            'DoctorPh': _('Phone No.'),
            'DoctorPwd':_('Password'),


        }
        widgets = {
            'DoctorMail': forms.EmailInput(attrs={'type': 'email', 'placeholder': 'Enter your email'}),
            'DoctorName': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'DoctorPh': forms.Textarea(attrs={'placeholder': 'Enter your address'}),
            'DoctorPwd': forms.TextInput(attrs={'placeholder': 'Enter your password'}),

        }



class LoginForm(forms.Form):
    mail= forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'mail-txt'}))
    pwd= forms.CharField(label='Password',widget=forms.PasswordInput)

class Updateform1(forms.Form):
    img =forms.ImageField()
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder':'Enter your name'}))
    mail =forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'type':'email','placeholder':'Enter your name'}))
    phno =forms.CharField(label='Phone no.',widget=forms.TextInput(attrs={'placeholder':'Enter your phone number'}))
    dob = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'placeholder':'Enter your date of birth'}))
    addr= forms.CharField(label='Address', widget=forms.Textarea(attrs={'placeholder':'Enter your address'}))
    pwd = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['ScheduleDate', 'ScheduleStartTime', 'ScheduleEndTime', 'MaxPatient']
        widgets = {'ScheduleDate': forms.DateInput(attrs={'type': 'date'}),
                   'ScheduleStartTime': forms.TimeInput(attrs={'type': 'time'}),
                   'ScheduleEndTime': forms.TimeInput(attrs={'type': 'time'}),
                   'MaxPatient': forms.NumberInput(attrs={'type': 'number','min':'0', 'max':'15'})
                   }

class DateForm(forms.Form):
    startDate = forms.DateField(label='From', widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd'}))
    endDate = forms.DateField(label='To', widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd'}))

#patients


class searchForm(forms.Form):
    radio_choices = [
        ("name", "Search by Name"),
        ("department", "Search by Department")
    ]
    searchby = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Choose search type:",
        choices=radio_choices,

    )

class PatientSignUpForm(forms.ModelForm):
    PatientPwd = forms.CharField(label='Password',widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    PatientDob = forms.DateField(label='Date of Birth',widget=forms.DateInput(attrs={'type': 'date'}))
    PatientPh = forms.CharField(max_length=30, label='Phone')


    class Meta:
        model = Patient
        fields = ['PatientName', 'PatientMail', 'PatientPh', 'PatientDob', 'PatientAddr', 'PatientPwd']
        widgets = {'PatientPwd': forms.PasswordInput(),
                   'PatientAddr':forms.Textarea()}
        labels = {
            'PatientName': 'Name',
            'PatientMail': 'Email',
            'PatientPh': 'Phone',
            'PatientDob': 'Date of Birth',
            'PatientAddr': 'Address',
            'PatientPwd': 'Password',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('PatientPwd')
        confirm_password = cleaned_data.get('confirm_password')
        patient_mail = cleaned_data.get('PatientMail')
        patient_ph = cleaned_data.get('PatientPh')

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")


        if Patient.objects.filter(PatientMail=patient_mail).exists():
            self.add_error('PatientMail', 'This email is already registered')


        if not patient_ph.isdigit():
            self.add_error('PatientPh', 'Phone number must contain only digits')

        if Patient.objects.filter(PatientPh=patient_ph).exists():
            self.add_error('PatientPh', 'This phone number is already registered')

        # Validate date of birth (optional)
        patient_dob = cleaned_data.get('PatientDob')
        if patient_dob and patient_dob.year < 1930:
            self.add_error('PatientDob', 'Please enter a valid date of birth')

        if len(password) < 8:
            self.add_error('PatientPwd', 'Password must be at least 8 characters long')


class DoctorSignUpForm(forms.ModelForm):
    DoctorPwd = forms.CharField(label='Password',widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    Department = forms.ModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = Doctor
        fields = ['DoctorName', 'DoctorMail', 'DoctorPh', 'Department', 'DoctorPwd']
        widgets = {'DoctorPwd': forms.PasswordInput()}
        labels = {
            'DoctorName': 'Name',
            'DoctorMail': 'Email',
            'DoctorPh': 'Phone',
            'DoctorPwd': 'Password',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('DoctorPwd')
        confirm_password = cleaned_data.get('confirm_password')
        doctor_mail = cleaned_data.get('DoctorMail')
        doctor_ph = cleaned_data.get('DoctorPh')

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        if Doctor.objects.filter(DoctorMail=doctor_mail).exists():
            self.add_error('DoctorMail', 'This email is already registered')

        if not doctor_ph.isdigit():
            self.add_error('DoctorPh', 'Phone number must contain only digits')

        if Doctor.objects.filter(DoctorPh=doctor_ph).exists():
            self.add_error('DoctorPh', 'This phone number is already registered')

        if len(password) < 8:
            self.add_error('DoctorPwd', 'Password must be at least 8 characters long')










