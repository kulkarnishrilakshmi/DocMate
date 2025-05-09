from django.contrib import admin
from .models import Patient, Doctor, Admin

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Admin)