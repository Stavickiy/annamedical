from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404

from rest_framework import generics, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serialisers import PatientSerializer, AppointmentSerializer, AppointmentDetailSerializer
from appointment.models import Appointment
from core.models import Patient, Doctor
from datetime import datetime, timedelta



class AppointmentsAPIList(LoginRequiredMixin, ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        doctor_pk = self.request.query_params.get('doc', None)
        # Получаем текущую дату
        current_date = datetime.now().date()

        # Определяем дату, на которую будет осуществлено отображение
        end_date = current_date + timedelta(days=7)

        # Фильтруем записи Appointment по полю date
        if doctor_pk:
            doctor = get_object_or_404(Doctor, pk=doctor_pk)
            appointments = doctor.appointments.filter(start__date__gte=current_date, start__date__lte=end_date)
        else:
            appointments = Appointment.objects.filter(start__date__gte=current_date, start__date__lte=end_date)
        return appointments


class AppointmentAPIView(LoginRequiredMixin, RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentDetailSerializer


class PatientsAPIList(LoginRequiredMixin, ListAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        doctor_pk = self.request.query_params.get('doc', None)
        if doctor_pk:
            doctor = get_object_or_404(Doctor, pk=doctor_pk)
            patients = doctor.patients.all()
        else:
            patients = Patient.objects.all()
        return patients
