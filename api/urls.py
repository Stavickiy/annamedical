from django.urls import path, include
from rest_framework import routers

from api.views import PatientsAPIList, DoctorPatientsAPIList, PatientsViewSet

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'patients', PatientsViewSet)


urlpatterns = [
    path('patients/<int:pk>/', DoctorPatientsAPIList.as_view(), name='doctor_patients'),
    path('patients/', PatientsAPIList.as_view(), name='all_patients'),
]