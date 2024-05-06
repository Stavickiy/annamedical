from django.urls import path
from . import views

app_name = 'appointment'

urlpatterns = [
    path('', views.Appointments.as_view(), name='appointments'),
    path('appointment_detail/<int:app_id>/', views.AppointmentDitail.as_view(), name='appointment_detail'),
    path('appointment_update/<int:pk>/', views.AppointmentUpdateView.as_view(), name='appointment_update'),
]
