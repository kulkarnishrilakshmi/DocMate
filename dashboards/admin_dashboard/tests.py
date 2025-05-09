from django.test import TestCase
from .models import Admin, Doctor, Patient

class AdminDashboardTests(TestCase):

    def setUp(self):
        self.admin = Admin.objects.create(username='admin', password='adminpass')
        self.doctor = Doctor.objects.create(username='doctor', password='doctorpass')
        self.patient = Patient.objects.create(username='patient', password='patientpass')

    def test_admin_can_view_doctors(self):
        response = self.client.get('/admin_dashboard/doctors/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.doctor.username)

    def test_admin_can_view_patients(self):
        response = self.client.get('/admin_dashboard/patients/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.patient.username)

    def test_admin_can_create_doctor(self):
        response = self.client.post('/admin_dashboard/doctors/create/', {
            'username': 'newdoctor',
            'password': 'newdoctorpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Doctor.objects.filter(username='newdoctor').exists())

    def test_admin_can_create_patient(self):
        response = self.client.post('/admin_dashboard/patients/create/', {
            'username': 'newpatient',
            'password': 'newpatientpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Patient.objects.filter(username='newpatient').exists())