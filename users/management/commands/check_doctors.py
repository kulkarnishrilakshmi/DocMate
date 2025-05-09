from django.core.management.base import BaseCommand
from users.models import Doctor

class Command(BaseCommand):
    help = 'Lists all doctor users and their permissions'

    def handle(self, *args, **options):
        doctors = Doctor.objects.all()
        if not doctors:
            self.stdout.write(self.style.WARNING('No doctors found in the database'))
            return
            
        self.stdout.write('Current Doctor Users:')
        for doctor in doctors:
            self.stdout.write(f'Username: {doctor.username}')
            self.stdout.write(f'Is Staff: {doctor.is_staff}')
            self.stdout.write(f'Is Superuser: {doctor.is_superuser}')
            self.stdout.write('---') 