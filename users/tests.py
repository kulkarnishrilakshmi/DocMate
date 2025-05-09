from django.test import TestCase
from .models import Patient, Doctor, Admin

class UserModelTests(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create_user(
            username='patient1',
            password='password123',
            email='patient1@example.com'
        )
        self.doctor = Doctor.objects.create_user(
            username='doctor1',
            password='password123',
            email='doctor1@example.com'
        )
        self.admin = Admin.objects.create_user(
            username='admin1',
            password='password123',
            email='admin1@example.com'
        )

    def test_patient_creation(self):
        self.assertEqual(self.patient.username, 'patient1')
        self.assertTrue(self.patient.check_password('password123'))

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.username, 'doctor1')
        self.assertTrue(self.doctor.check_password('password123'))

    def test_admin_creation(self):
        self.assertEqual(self.admin.username, 'admin1')
        self.assertTrue(self.admin.check_password('password123'))

    def test_patient_email(self):
        self.assertEqual(self.patient.email, 'patient1@example.com')

    def test_doctor_email(self):
        self.assertEqual(self.doctor.email, 'doctor1@example.com')

    def test_admin_email(self):
        self.assertEqual(self.admin.email, 'admin1@example.com')