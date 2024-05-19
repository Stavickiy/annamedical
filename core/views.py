from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from django.utils import timezone
from datetime import datetime, timedelta

from appointment.models import Appointment
from users.models import User
from .models import Doctor, Patient, Clinic


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    extra_context = {'title': 'Менеджмент пациентов'}


class IndexPage(LoginRequiredMixin, TemplateView):
    template_name = 'new/index.html'
    extra_context = {'title': 'Менеджмент пациентов'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # получаем id клиник в которых работает доктор(user)
        user = self.request.user
        clinics_ids = Doctor.objects.get(id=user.doctor.id).clinic.values_list('id', flat=True)

        # Получаем текущую дату без учета времени
        current_date = datetime.now().date()
        # Определяем начальную и конечную дату для фильтрации записей на сегодня
        start_of_day = datetime.combine(current_date, datetime.min.time())
        end_of_day = datetime.combine(current_date, datetime.max.time())
        # Фильтруем записи Appointment по полю start и клинике доктора
        appointments = Appointment.objects.filter(start__range=(start_of_day, end_of_day),
                                                  clinic__id__in=clinics_ids).exclude(status='canceled')
        context['appointments'] = appointments

        end_date = current_date + timedelta(days=7)
        # Фильтруем записи Appointment по полю start и клинике доктора
        appointments_week = Appointment.objects.filter(
            start__gte=current_date,
            start__lte=end_date,
            clinic__id__in=clinics_ids
        )
        context['appointments_week'] = appointments_week
        return context


class DoctorsPage(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'doctors.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        doctors = Doctor.objects.all()
        return doctors


class ServicePage(LoginRequiredMixin, TemplateView):
    template_name = 'services.html'
    extra_context = {'title': 'Наши услуги'}


class PatientsPage(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'new/patients.html'
    context_object_name = 'patients'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = Doctor.objects.all()
        context['clinics'] = Clinic.objects.all()
        return context

    def get_queryset(self):
        user = self.request.user
        clinics_ids = Doctor.objects.get(id=user.doctor.id).clinic.values_list('id', flat=True)
        return Patient.objects.filter(clinic__id__in=clinics_ids)


class PatientDetail(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patient.html'
    context_object_name = 'patient'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем текущую дату и время
        current_datetime = timezone.now()
        patient = context['patient']
        appointments = patient.appointments.all()
        prefetched_appointments = Appointment.objects.prefetch_related('services').filter(
            id__in=appointments.values_list('id', flat=True)).order_by('-start')

        context['appointments'] = list(patient.appointments.all().prefetch_related('photos').order_by('-start'))
        context['three_appointments'] = prefetched_appointments[:3]
        return context


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'new/user_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Получаем текущую дату без учета времени
        current_date = datetime.now().date()
        # Определяем начальную и конечную дату для фильтрации записей на сегодня
        start_of_day = datetime.combine(current_date, datetime.min.time())
        end_of_day = datetime.combine(current_date, datetime.max.time())
        context['appointments'] = Appointment.objects.filter(start__range=(start_of_day, end_of_day),
                                                             doctor=user.doctor).exclude(status='canceled')
        return context
