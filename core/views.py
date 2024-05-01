from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from django.utils import timezone
from datetime import timedelta

from appointment.models import Appointment
from .models import Doctor, Patient


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    extra_context = {'title': 'Менеджмент пациентов'}

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
    template_name = 'patients.html'
    context_object_name = 'patients'


class PatientDetail(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patient.html'
    context_object_name = 'patient'

    def get_context_data(self, *, object_list=None, **kwargs):
        # Получаем текущую дату и время
        current_datetime = timezone.now()
        context = super().get_context_data(**kwargs)
        patient = context['patient']
        appointments = patient.appointments.all()
        prefetched_appointments = Appointment.objects.prefetch_related('services').filter(
            id__in=appointments.values_list('id', flat=True)).order_by('-start')

        context['appointments'] = list(patient.appointments.all().order_by('-start'))
        context['three_appointments'] = prefetched_appointments[:3]
        return context
