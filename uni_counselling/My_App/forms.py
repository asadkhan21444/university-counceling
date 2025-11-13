# my_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser,Student
from .models import (
    Counsellor,
    Appointment,
    CounsellorAvailability,
    CounsellingSession,
    SessionDocument,
    EmergencyContact
)
###############################################################################################################
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role', 
                 'phone_number', 'date_of_birth', 'profile_picture', 
                 'first_name', 'last_name')
    
    def __init__(self, *args, **kwargs):
        admin_exists = kwargs.pop('admin_exists', False)
        super().__init__(*args, **kwargs)
        
        # Remove admin role if admin already exists
        if admin_exists:
            self.fields['role'].choices = [
                choice for choice in self.fields['role'].choices 
                if choice[0] != 'admin'
            ]
        
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['profile_picture']:
                field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'role':
                field.widget.attrs.update({'class': 'form-select'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
###############################################################################################################
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
###############################################################################################################
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id', 'enrollment_date', 'faculty', 'department',
            'academic_year', 'emergency_contact_name', 'emergency_contact_phone', 'address'
        ]
        widgets = {
            'enrollment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'faculty': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
########################################################################################################################
class CounsellorForm(forms.ModelForm):
    class Meta:
        model = Counsellor
        fields = "__all__"
        widgets = {
            "specialization": forms.TextInput(attrs={"class": "form-control"}),
            "license_number": forms.TextInput(attrs={"class": "form-control"}),
            "experience_years": forms.NumberInput(attrs={"class": "form-control"}),
            "qualifications": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "area_of_expertise": forms.Select(attrs={"class": "form-control"}),
            "is_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "max_students": forms.NumberInput(attrs={"class": "form-control"}),
        }
#############################################################################################################################
class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Appointment
        fields = ['student', 'counsellor', 'appointment_date', 'duration_minutes', 'status', 'purpose', 'concerns']
#############################################################################################################################
class CounsellorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = CounsellorAvailability
        fields = ["counsellor", "day_of_week", "start_time", "end_time", "is_active"]
        widgets = {
            "day_of_week": forms.Select(attrs={"class": "form-control"}),
            "counsellor": forms.Select(attrs={"class": "form-control"}),
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "end_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
###########################################################################################################################
class SessionDocumentForm(forms.ModelForm):
    class Meta:
        model = SessionDocument
        fields = ['session', 'document_type', 'file', 'file_name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file_name': forms.TextInput(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'session': forms.Select(attrs={'class': 'form-select'}),
        }
##############################################################################################################################
class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['student', 'name', 'relationship', 'phone_number', 'email', 'is_primary']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
#############################################################################################
