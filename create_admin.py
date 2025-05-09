import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appointment_system.settings')
django.setup()

from users.models import Admin

def create_admin_user():
    try:
        # Check if admin user already exists
        if not Admin.objects.filter(username='admin').exists():
            # Create admin user
            admin = Admin.objects.create(
                username='admin',
                email='admin@example.com',
                is_staff=True,
                is_superuser=True
            )
            # Set password securely
            admin.set_password('admin123')
            admin.save()
            
            print("Admin user created successfully!")
            print("Username: admin")
            print("Password: admin123")
        else:
            # Update existing admin password
            admin = Admin.objects.get(username='admin')
            admin.set_password('admin123')
            admin.save()
            print("Admin password updated successfully!")
            print("Username: admin")
            print("Password: admin123")
    except Exception as e:
        print(f"Error creating/updating admin user: {str(e)}")

if __name__ == '__main__':
    create_admin_user() 