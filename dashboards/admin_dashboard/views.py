from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth import logout
from users.models import Patient, Doctor
from dashboards.patient_dashboard.models import AppointmentRequest as Appointment
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from dashboards.doctor_dashboard.models import Appointment as DoctorAppointment

@login_required
def admin_dashboard(request):
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending')
    
    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
    }
    
    return render(request, 'admin_dashboard/dashboard.html', context)

@login_required
def manage_patients(request):
    patients = Patient.objects.all()
    return render(request, 'admin_dashboard/manage_patients.html', {'patients': patients})

@login_required
def manage_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin_dashboard/manage_doctors.html', {'doctors': doctors})

@login_required
def manage_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'admin_dashboard/manage_appointments.html', {'appointments': appointments})

@login_required
def manage_appointment_requests(request):
    pending_requests = Appointment.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'admin_dashboard/manage_appointment_requests.html', {
        'pending_requests': pending_requests
    })

def send_welcome_email(doctor, password):
    """Send a welcome email to a new doctor."""
    context = {
        'doctor': doctor,
        'password': password,
        'login_url': settings.SITE_URL + reverse('doctor_dashboard:dashboard')
    }
    
    html_message = render_to_string('email/welcome_doctor.html', context)
    plain_message = strip_tags(html_message)
    
    subject = f'Welcome to DocMate - Your Doctor Account'
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[doctor.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_appointment_confirmation(appointment):
    """Send appointment confirmation email to patient."""
    context = {
        'patient': appointment.patient,
        'doctor': appointment.doctor,
        'appointment': appointment,
        'appointment_url': settings.SITE_URL + reverse('patient_dashboard:appointment_detail', args=[appointment.id])
    }
    
    html_message = render_to_string('email/appointment_confirmation.html', context)
    plain_message = strip_tags(html_message)
    
    subject = f'Appointment Confirmation - {appointment.date}'
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[appointment.patient.email],
        html_message=html_message,
        fail_silently=False,
    )

@login_required
def add_doctor(request):
    if request.method == 'POST':
        try:
            # Use default password
            default_password = 'DocMate@123'
            
            # Create the doctor
            doctor = Doctor.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=default_password,
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                specialization=request.POST['specialization'],
                phone_number=request.POST['phone_number'],
                bio=request.POST.get('bio', '')
            )
            
            messages.success(request, f'Doctor {doctor.username} has been added successfully with default password: {default_password}')
            return redirect('admin_dashboard:manage_doctors')
            
        except Exception as e:
            messages.error(request, f'Error adding doctor: {str(e)}')
    
    return render(request, 'admin_dashboard/add_doctor.html')

@login_required
def view_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'admin_dashboard/view_patient.html', {'patient': patient})

@login_required
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        try:
            # Update patient information
            patient.username = request.POST['username']
            patient.email = request.POST['email']
            patient.first_name = request.POST['first_name']
            patient.last_name = request.POST['last_name']
            patient.date_of_birth = request.POST.get('date_of_birth')
            patient.phone_number = request.POST.get('phone_number')
            patient.address = request.POST.get('address')
            patient.is_active = request.POST.get('is_active') == 'on'
            
            patient.save()
            messages.success(request, 'Patient information updated successfully.')
            return redirect('admin_dashboard:view_patient', patient_id=patient.id)
            
        except Exception as e:
            messages.error(request, f'Error updating patient: {str(e)}')
    
    return render(request, 'admin_dashboard/edit_patient.html', {'patient': patient})

@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        try:
            username = patient.username
            patient.delete()
            messages.success(request, f'Patient {username} has been deleted successfully.')
            return redirect('admin_dashboard:manage_patients')
        except Exception as e:
            messages.error(request, f'Error deleting patient: {str(e)}')
    
    return redirect('admin_dashboard:view_patient', patient_id=patient.id)

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('users:login')
    return render(request, 'admin_dashboard/logout_confirm.html')

@login_required
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    try:
        username = doctor.username
        doctor.delete()
        messages.success(request, f'Doctor {username} has been deleted successfully.')
    except Exception as e:
        messages.error(request, f'Error deleting doctor: {str(e)}')
    return redirect('admin_dashboard:manage_doctors')

@login_required
def view_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    # Get doctor's appointments from both models
    admin_appointments = Appointment.objects.filter(doctor=doctor)
    doctor_appointments = DoctorAppointment.objects.filter(doctor=doctor)
    
    # Combine appointments
    appointments = list(admin_appointments) + list(doctor_appointments)
    
    # Calculate statistics
    total_appointments = len(appointments)
    active_appointments = sum(1 for a in appointments if a.status == 'scheduled')
    completed_appointments = sum(1 for a in appointments if a.status == 'completed')
    cancelled_appointments = sum(1 for a in appointments if a.status == 'canceled')
    
    # Get recent reviews if available
    reviews = getattr(doctor, 'reviews', [])[:5] if hasattr(doctor, 'reviews') else []
    
    # Get availability data
    availability = getattr(doctor, 'availability', {})
    if isinstance(availability, str):
        try:
            import json
            availability = json.loads(availability)
        except:
            availability = {}
    
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'total_appointments': total_appointments,
        'active_appointments': active_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'reviews': reviews,
        'languages': doctor.languages.split(',') if doctor.languages else [],
        'insurance_providers': doctor.insurance_providers.split(',') if doctor.insurance_providers else [],
        'availability': availability,
        'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    }
    return render(request, 'admin_dashboard/view_doctor.html', context)

@login_required
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        try:
            # Update basic information
            doctor.username = request.POST.get('username')
            doctor.email = request.POST.get('email')
            doctor.first_name = request.POST.get('first_name')
            doctor.last_name = request.POST.get('last_name')
            doctor.specialization = request.POST.get('specialization')
            doctor.phone_number = request.POST.get('phone_number')
            doctor.bio = request.POST.get('bio')
            doctor.experience = request.POST.get('experience')
            doctor.qualifications = request.POST.get('qualifications')
            doctor.is_active = request.POST.get('is_active') == 'on'
            
            # Handle profile picture
            if 'profile_picture' in request.FILES:
                doctor.profile_picture = request.FILES['profile_picture']
            
            # Handle languages
            languages = request.POST.getlist('languages')
            doctor.languages = ','.join(languages) if languages else ''
            
            # Handle insurance providers
            insurance_providers = request.POST.getlist('insurance_providers')
            doctor.insurance_providers = ','.join(insurance_providers) if insurance_providers else ''
            
            # Handle availability
            availability = {}
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                if request.POST.get(f'{day}_available') == 'on':
                    availability[day] = {
                        'start': request.POST.get(f'{day}_start'),
                        'end': request.POST.get(f'{day}_end')
                    }
            doctor.availability = availability
            
            # Save changes
            doctor.save()
            messages.success(request, 'Doctor information updated successfully.')
            return redirect('admin_dashboard:view_doctor', doctor_id=doctor.id)
            
        except Exception as e:
            messages.error(request, f'Error updating doctor: {str(e)}')
    
    # Prepare context with all necessary data
    context = {
        'doctor': doctor,
        'specializations': [
            'Cardiology', 'Dermatology', 'Endocrinology', 'Gastroenterology',
            'General Medicine', 'Neurology', 'Obstetrics and Gynecology',
            'Ophthalmology', 'Orthopedics', 'Pediatrics', 'Psychiatry',
            'Radiology', 'Urology'
        ],
        'languages': [
            'Hindi', 'English', 'Bengali', 'Telugu', 'Marathi', 'Tamil',
            'Urdu', 'Gujarati', 'Kannada', 'Odia', 'Malayalam', 'Punjabi',
            'Sanskrit', 'Assamese', 'Sindhi', 'Nepali', 'Konkani', 'Manipuri',
            'Bodo', 'Dogri', 'Kashmiri', 'Santhali', 'Maithili'
        ],
        'insurance_providers': [
            'Aetna', 'Blue Cross Blue Shield', 'Cigna', 'UnitedHealthcare',
            'Medicare', 'Medicaid', 'Kaiser Permanente', 'Humana',
            'Anthem', 'Other'
        ],
        'time_slots': [
            '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
            '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
            '15:00', '15:30', '16:00', '16:30', '17:00', '17:30'
        ],
        'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    }
    return render(request, 'admin_dashboard/edit_doctor.html', context)

@login_required
def accept_appointment_request(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        try:
            # Create a new appointment in the doctor's dashboard
            doctor_appointment = DoctorAppointment.objects.create(
                patient=appointment.patient,
                doctor=appointment.doctor,
                appointment_datetime=appointment.appointment_datetime,
                status='scheduled',
                reason=appointment.reason,
                notes=appointment.notes
            )
            
            # Update the original appointment request
            appointment.status = 'accepted'
            appointment.save()
            
            # Send confirmation email to patient
            send_appointment_confirmation(doctor_appointment)
            
            messages.success(request, 'Appointment request has been accepted and scheduled.')
            return redirect('admin_dashboard:manage_appointment_requests')
            
        except Exception as e:
            messages.error(request, f'Error accepting appointment: {str(e)}')
    
    return render(request, 'admin_dashboard/view_appointment_request.html', {
        'appointment': appointment
    })

@login_required
def reject_appointment_request(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        try:
            appointment.status = 'rejected'
            appointment.save()
            
            # Send rejection email to patient
            context = {
                'patient': appointment.patient,
                'doctor': appointment.doctor,
                'appointment': appointment
            }
            
            html_message = render_to_string('email/appointment_rejected.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject='Appointment Request Rejected',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[appointment.patient.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Appointment request has been rejected.')
            return redirect('admin_dashboard:manage_appointment_requests')
            
        except Exception as e:
            messages.error(request, f'Error rejecting appointment: {str(e)}')
    
    return render(request, 'admin_dashboard/view_appointment_request.html', {
        'appointment': appointment
    })