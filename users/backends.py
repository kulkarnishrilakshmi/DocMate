from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Patient, Doctor, Admin
from django.core.exceptions import PermissionDenied

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Try to find the user in each model
        try:
            # Try Patient first
            user = Patient.objects.get(username=username)
            if user.check_password(password):
                return user
        except Patient.DoesNotExist:
            try:
                # Try Doctor next
                user = Doctor.objects.get(username=username)
                if user.check_password(password):
                    return user
            except Doctor.DoesNotExist:
                try:
                    # Try Admin last
                    user = Admin.objects.get(username=username)
                    if user.check_password(password):
                        return user
                except Admin.DoesNotExist:
                    return None
        return None

    def get_user(self, user_id):
        # Try to get the user from each model
        try:
            return Patient.objects.get(pk=user_id)
        except Patient.DoesNotExist:
            try:
                return Doctor.objects.get(pk=user_id)
            except Doctor.DoesNotExist:
                try:
                    return Admin.objects.get(pk=user_id)
                except Admin.DoesNotExist:
                    return None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        print(f"Checking if user can authenticate: {user.username}, is_active: {is_active}")  # Debug log
        return is_active or is_active is None 