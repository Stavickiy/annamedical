
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from rest_framework import generics, viewsets, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView, \
    CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serialisers import PatientSerializer, AppointmentSerializer, AppointmentDetailSerializer, \
    PatientUpdateSerializer, ServiceSerializer, AppointmentMediaSerializer, AppointmentItemSerializer
from appointment.models import Appointment, AppointmentItem, Media
from core.models import Patient, Doctor, Service
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


class CreateAppointmentAPIView(generics.CreateAPIView):
    serializer_class = AppointmentDetailSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        items_data = request.data.getlist('items', [])
        appointment_data = request.data
        serializer = self.get_serializer(data=appointment_data)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()

        # Добавление услуг к созданному назначению
        for service_id in items_data:
            service = Service.objects.get(id=service_id)
            AppointmentItem.objects.create(
                appointment=appointment,
                service=service,
                quantity=1,  # По умолчанию количество 1
                price=service.cost  # Используем стоимость из базы данных
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AppointmentAPIUpdate(UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentDetailSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Обновление услуг, связанных с назначением
        items_data = request.data.getlist('items', [])
        instance.items.all().delete()  # Удаление всех предыдущих записей
        for service_id in items_data:
            service = Service.objects.get(id=service_id)
            AppointmentItem.objects.create(
                appointment=instance,
                service=service,
                quantity=1,
                price=service.cost
            )

        return Response(serializer.data)

class UpdateItemAPIView(UpdateAPIView):
    queryset = AppointmentItem.objects.all()
    serializer_class = AppointmentItemSerializer
    permission_classes = [IsAuthenticated]


class CreateServiceAPIView(ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]


class AddedAppointmentPhotoAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        medias = request.FILES.getlist('medias')
        appointment_id = request.data.get('appointment')

        if not medias or not appointment_id:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_media = []
        for media in medias:
            if media.content_type.startswith('image/'):
                media_instance = Media(appointment_id=appointment_id, photo=media)
            elif media.content_type.startswith('video/'):
                media_instance = Media(appointment_id=appointment_id, video=media)
            else:
                continue

            media_instance.save()
            uploaded_media.append(AppointmentMediaSerializer(media_instance).data)

        return Response(uploaded_media, status=status.HTTP_201_CREATED)
