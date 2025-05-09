from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, Doctor, Admin

class PatientRegistrationForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'address')
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'date_of_birth': 'Date of Birth',
            'phone_number': 'Phone Number',
            'address': 'Address',
        }

class DoctorRegistrationForm(UserCreationForm):
    class Meta:
        model = Doctor
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'specialization', 'phone_number', 'bio')
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'specialization': 'Specialization',
            'phone_number': 'Phone Number',
            'bio': 'Bio',
        }

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        } 