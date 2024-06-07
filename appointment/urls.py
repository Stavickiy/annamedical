from django.urls import path
from . import views
from .views import UpdateAppointmentItemsView

app_name = 'appointment'

urlpatterns = [
    path('create_appointment/', views.CreateAppointmentVew.as_view(), name='create_appointment'),
    path('appointment_detail/<int:pk>/', views.AppointmentDitail.as_view(), name='appointment_detail'),
    path('appointments/<int:pk>/update-items/', UpdateAppointmentItemsView.as_view(), name='update_appointment_items'),
    # path('appointment_update/<int:pk>/', views.AppointmentUpdateView.as_view(), name='appointment_update'),
]
