from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('index/', views.IndexPage.as_view(), name='index'),
    path('doctors/', views.DoctorsPage.as_view(), name='doctors'),
    path('services/', views.ServicePage.as_view(), name='services'),
    path('patients/', views.PatientsPage.as_view(), name='patients'),
    path('patient_detail/<int:pk>/', views.PatientDetail.as_view(), name='patient_detail'),
    path('user_profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
]
