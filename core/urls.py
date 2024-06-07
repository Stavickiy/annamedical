from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('patients/', views.PatientsPage.as_view(), name='patients'),
    path('patient_detail/<int:pk>/', views.PatientDetail.as_view(), name='patient_detail'),
    path('user_profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('add_patient/', views.AddPatientView.as_view(), name='add_patient'),
    path('services/', views.ServicesView.as_view(), name='services'),
]
