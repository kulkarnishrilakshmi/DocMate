from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Patient, Doctor, Admin
from .forms import PatientRegistrationForm, DoctorRegistrationForm, AdminRegistrationForm
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('users:login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'patient')  # Default to patient if not specified
        next_url = request.GET.get('next', None)
        
        # Debug messages
        print(f"Login attempt - Username: {username}, User Type: {user_type}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Debug messages
            print(f"User authenticated: {user}")
            print(f"User type: {type(user)}")
            print(f"is_staff: {user.is_staff}")
            print(f"is_superuser: {user.is_superuser}")
            print(f"hasattr(admin): {hasattr(user, 'admin')}")
            
            # Check if the user type matches
            if user_type == 'patient':
                if isinstance(user, Patient):
                    login(request, user)
                    messages.success(request, 'Successfully logged in as patient.')
                    return redirect(next_url or 'patient_dashboard:dashboard')
                else:
                    messages.error(request, 'This account is not a patient account.')
                    return redirect('users:login')
            elif user_type == 'doctor':
                if isinstance(user, Doctor):
                    login(request, user)
                    messages.success(request, 'Successfully logged in as doctor.')
                    return redirect(next_url or 'doctor_dashboard:dashboard')
                else:
                    messages.error(request, 'This account is not a doctor account.')
                    return redirect('users:login')
            elif user_type == 'admin':
                # Check if user is an admin using multiple methods
                is_admin = (
                    isinstance(user, Admin) or  # Direct instance check
                    Admin.is_admin_user(user) or  # Using the class method
                    (user.is_staff and user.is_superuser)  # Permission check
                )
                
                if is_admin:
                    login(request, user)
                    messages.success(request, 'Successfully logged in as admin.')
                    return redirect(next_url or 'admin_dashboard:dashboard')
                else:
                    messages.error(request, 'This account is not an admin account.')
                    return redirect('users:login')
            else:
                messages.error(request, f'Invalid user type. Please select the correct user type.')
                return redirect('users:login')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('users:login')
    
    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='users.backends.CustomUserBackend')
            return redirect('patient_dashboard:dashboard')
    else:
        form = PatientRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Update profile information
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        
        if hasattr(user, 'date_of_birth'):
            user.date_of_birth = request.POST.get('date_of_birth', user.date_of_birth)
        if hasattr(user, 'address'):
            user.address = request.POST.get('address', user.address)
        
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('users:profile')
    
    return render(request, 'profile.html', {'user': request.user})

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = request.user
        
        # Check if current password is correct
        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('users:profile')
        
        # Check if new passwords match
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('users:profile')
        
        # Change password
        user.set_password(new_password)
        user.save()
        
        # Update session to prevent logout
        update_session_auth_hash(request, user)
        
        messages.success(request, 'Password changed successfully.')
        return redirect('users:profile')
    
    return redirect('users:profile')

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save()
            login(request, patient, backend='users.backends.CustomUserBackend')
            return redirect('patient_dashboard:dashboard')
    else:
        form = PatientRegistrationForm()
    return render(request, 'register_patient.html', {'form': form})

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            login(request, doctor, backend='users.backends.CustomUserBackend')
            return redirect('doctor_dashboard:dashboard')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'register_doctor.html', {'form': form})

def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            login(request, admin, backend='users.backends.CustomUserBackend')
            return redirect('admin_dashboard:dashboard')
    else:
        form = AdminRegistrationForm()
    return render(request, 'register_admin.html', {'form': form})

@login_required
def user_profile(request):
    return render(request, 'user_profile.html')