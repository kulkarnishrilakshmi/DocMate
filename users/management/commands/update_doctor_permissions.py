from django.core.management.base import BaseCommand
from users.models import Doctor

class Command(BaseCommand):
    help = 'Updates existing doctor users to have non-admin access'

    def handle(self, *args, **options):
        doctors = Doctor.objects.filter(is_staff=True)
        count = 0
        
        for doctor in doctors:
            doctor.is_staff = False
            doctor.is_superuser = False
            doctor.save()
            count += 1
            self.stdout.write(f'Updated doctor: {doctor.username}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} doctors to non-admin access')) 