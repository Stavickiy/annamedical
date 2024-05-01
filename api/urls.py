from django.urls import path, include
from rest_framework import routers

from api.views import PatientsAPIList, AppointmentsAPIList

app_name = 'api'

# router = routers.SimpleRouter()
# router.register(r'patients', PatientsViewSet)


urlpatterns = [
    path('patients/', PatientsAPIList.as_view(), name='patients'),
    path('appointments/', AppointmentsAPIList.as_view(), name='all_appointments'),
]
