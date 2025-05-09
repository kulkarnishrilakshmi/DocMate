from django.core.management.base import BaseCommand
from users.models import Admin
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser admin account'

    def handle(self, *args, **options):
        try:
            # First check if any admin exists
            if Admin.objects.exists():
                self.stdout.write(self.style.WARNING('Admin user(s) already exist in the database.'))
                return

            # Create the admin user
            admin = Admin.objects.create_superuser(
                username='admin',
                email='admin@docmate.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            
            # Verify the admin was created correctly
            if admin.is_staff and admin.is_superuser:
                self.stdout.write(self.style.SUCCESS(
                    'Successfully created admin user with the following credentials:\n'
                    'Username: admin\n'
                    'Password: admin123\n'
                    'Email: admin@docmate.com'
                ))
            else:
                self.stdout.write(self.style.ERROR('Admin user was created but does not have proper permissions.'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating admin user: {str(e)}')) 