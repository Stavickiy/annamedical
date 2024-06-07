from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from appointment.models import Appointment
from .models import Doctor, Patient

class ClinicAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        patient = get_object_or_404(Patient, pk=kwargs['pk'])
        user = request.user
        doctor = user.doctor
        clinics = doctor.clinic.all()

        if patient.clinic not in clinics:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class ClinicAppointmentAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=kwargs['pk'])
        user = request.user
        doctor = user.doctor
        clinics = doctor.clinic.all()

        if appointment.clinic not in clinics:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
