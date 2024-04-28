from django.contrib import admin
from django.urls import path, include

from api.views import PatientAPIList

app_name = 'api'

urlpatterns = [
    path('patients/', PatientAPIList.as_view(), name='patients'),
]