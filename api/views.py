from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from rest_framework import generics, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView, \
    CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serialisers import PatientSerializer, AppointmentSerializer, AppointmentDetailSerializer, \
    PatientUpdateSerializer
from appointment.models import Appointment
from core.models import Patient, Doctor
from datetime import datetime, timedelta



class AppointmentsAPIList(LoginRequiredMixin, ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        appointments = Appointment.objects.all()

        # Получение параметров фильтрации из query string
        doctor_id = self.request.query_params.get('doctor_id')
        clinic_id = self.request.query_params.get('clinic_id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        # Фильтрация по доктору, если передан doctor_id
        if doctor_id and doctor_id != 'Доктор':
            appointments = appointments.filter(doctor_id=doctor_id)

        # Фильтрация по клинике, если передан clinic_id
        if clinic_id and clinic_id != 'Клиника':
            appointments = appointments.filter(clinic_id=clinic_id)

        # Фильтрация по дате от, если передан start_date
        if start_date:
            start_date_time = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            appointments = appointments.filter(start__gte=start_date_time)

        # Фильтрация по дате до, если передан end_date
        if end_date:
            end_date_time = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d')) + timedelta(days=1)
            appointments = appointments.filter(end__lte=end_date_time)

        return appointments

    # def get_queryset(self):
    #     doctor_pk = self.request.query_params.get('doc', None)
    #     # Получаем текущую дату
    #     current_date = datetime.now().date()
    #
    #     # Определяем дату, на которую будет осуществлено отображение
    #     end_date = current_date + timedelta(days=7)
    #
    #     # Фильтруем записи Appointment по полю date
    #     if doctor_pk:
    #         doctor = get_object_or_404(Doctor, pk=doctor_pk)
    #         appointments = doctor.appointments.filter(start__date__gte=current_date, start__date__lte=end_date)
    #     else:
    #         appointments = Appointment.objects.filter(start__date__gte=current_date, start__date__lte=end_date)
    #     return appointments


class AppointmentAPIView(LoginRequiredMixin, RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentDetailSerializer


class PatientsAPIList(LoginRequiredMixin, ListAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        patients = Patient.objects.all()

        # Получение параметров фильтрации из query string
        doctor_id = self.request.query_params.get('doctor_id')
        clinic_id = self.request.query_params.get('clinic_id')

        # Фильтрация по доктору, если передан doctor_id
        if doctor_id and doctor_id != 'Доктор':
            patients = patients.filter(doctor_id=doctor_id)

        # Фильтрация по клинике, если передан clinic_id
        if clinic_id and clinic_id != 'Клиника':
            patients = patients.filter(clinic_id=clinic_id)

        return patients

class PatientUpdate(UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()

class CreatePatientAPIView(ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientUpdateSerializer
    permission_classes = [IsAuthenticated]

class CreateAppointmentAPIView(ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = PatientUpdateSerializer
    permission_classes = [IsAuthenticated]
