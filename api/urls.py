from django.urls import path, include
from rest_framework import routers

from api.views import PatientsAPIList, AppointmentsAPIList, AppointmentAPIView

app_name = 'api'


urlpatterns = [
    path('patients_list/', PatientsAPIList.as_view(), name='patients_list'),
    path('appointments/', AppointmentsAPIList.as_view(), name='all_appointments'),
    path('appointment/<int:pk>', AppointmentAPIView.as_view(), name='appointment_view'),
]
