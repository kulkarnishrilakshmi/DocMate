from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('admin-dashboard/', include('dashboards.admin_dashboard.urls')),
    path('doctor-dashboard/', include('dashboards.doctor_dashboard.urls')),
    path('patient-dashboard/', include('dashboards.patient_dashboard.urls')),
    path('users/', include('users.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)