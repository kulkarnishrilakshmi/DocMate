from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class Patient(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'patient'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='patient_set',
        blank=True,
        help_text='The groups this patient belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='patient_set',
        blank=True,
        help_text='Specific permissions for this patient.',
        verbose_name='user permissions',
    )

class Doctor(AbstractUser):
    specialization = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_ratings = models.IntegerField(default=0)

    class Meta:
        db_table = 'doctor'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='doctor_set',
        blank=True,
        help_text='The groups this doctor belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='doctor_set',
        blank=True,
        help_text='Specific permissions for this doctor.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.specialization})"

    def update_rating(self, new_rating):
        """Update doctor's rating when a new rating is added"""
        self.total_ratings += 1
        self.rating = ((self.rating * (self.total_ratings - 1)) + new_rating) / self.total_ratings
        self.save()

class Admin(AbstractUser):
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    admin_level = models.CharField(max_length=50, default='standard')

    class Meta:
        db_table = 'admin'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='admin_set',
        blank=True,
        help_text='The groups this admin belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='admin_set',
        blank=True,
        help_text='Specific permissions for this admin.',
        verbose_name='user permissions',
    )

    def save(self, *args, **kwargs):
        self.is_staff = True
        self.is_superuser = True
        super().save(*args, **kwargs)

    @classmethod
    def is_admin_user(cls, user):
        return hasattr(user, 'admin') or (user.is_staff and user.is_superuser)

    class AdminManager(UserManager):
        def create_user(self, username, email=None, password=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            return super().create_user(username, email, password, **extra_fields)

        def create_superuser(self, username, email=None, password=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            return super().create_superuser(username, email, password, **extra_fields)

    objects = AdminManager()