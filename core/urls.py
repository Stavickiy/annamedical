from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('doctors/', views.DoctorsPage.as_view(), name='doctors'),
    path('services/', views.ServicePage.as_view(), name='services'),
    path('patients/', views.PatientsPage.as_view(), name='patients'),
]
