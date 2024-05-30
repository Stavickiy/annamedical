from django.urls import path, include
from rest_framework import routers

from api.views import PatientsAPIList, AppointmentsAPIList, AppointmentAPIView, PatientUpdate, CreatePatientAPIView, \
    CreateAppointmentAPIView, CreateServiceAPIView, AppointmentAPIUpdate, AddedAppointmentPhotoAPI, UpdateItemAPIView

app_name = 'api'

urlpatterns = [
    path('patients_list/', PatientsAPIList.as_view(), name='patients_list'),
    path('patient/<int:pk>/update/', PatientUpdate.as_view(), name='patient_update'),
    path('appointments/', AppointmentsAPIList.as_view(), name='all_appointments'),
    path('appointment/<int:pk>', AppointmentAPIView.as_view(), name='appointment_view'),
    path('create_patient/', CreatePatientAPIView.as_view(), name='create_patient'),
    path('create_appointment/', CreateAppointmentAPIView.as_view(), name='create_appointment'),
    path('create_service/', CreateServiceAPIView.as_view(), name='create_service'),
    path('appointment/<int:pk>/update/', AppointmentAPIUpdate.as_view(), name='appointment_update'),
    path('appointment/adding_photo/', AddedAppointmentPhotoAPI.as_view(), name='adding_appointment_photo'),
    path('appointment_item/<int:pk>/update/', UpdateItemAPIView.as_view(), name='appointment_item_update'),
]
