import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appointment_system.settings')
django.setup()

from users.models import Admin

def fix_admin():
    try:
        # Delete existing admin user if exists
        Admin.objects.filter(username='admin').delete()
        
        # Create new admin user using create_superuser
        admin = Admin.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")

if __name__ == '__main__':
    fix_admin() 