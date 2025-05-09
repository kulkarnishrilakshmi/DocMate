from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('appointments/', views.manage_appointments, name='manage_appointments'),
    path('appointment-requests/', views.manage_appointment_requests, name='manage_appointment_requests'),
    path('appointment-requests/<int:appointment_id>/accept/', views.accept_appointment_request, name='accept_appointment_request'),
    path('appointment-requests/<int:appointment_id>/reject/', views.reject_appointment_request, name='reject_appointment_request'),
    path('patients/', views.manage_patients, name='manage_patients'),
    path('patients/<int:patient_id>/', views.view_patient, name='view_patient'),
    path('patients/<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('patients/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),
    path('doctors/', views.manage_doctors, name='manage_doctors'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/<int:doctor_id>/', views.view_doctor, name='view_doctor'),
    path('doctors/<int:doctor_id>/edit/', views.edit_doctor, name='edit_doctor'),
    path('doctors/<int:doctor_id>/delete/', views.delete_doctor, name='delete_doctor'),
    path('logout/', views.logout_view, name='logout'),
]