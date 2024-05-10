from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView

from appointment.forms import AppointmentForm
from appointment.models import Appointment
from core.models import Service, Doctor, Clinic
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse


class Appointments(ListView):
    model = Appointment
    template_name = 'appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        # Получаем текущую дату и время
        current_datetime = timezone.now()
        # Определяем дату, на которую будет осуществлено отображение
        end_date = current_datetime + timedelta(days=7)
        # Фильтруем записи Appointment по полю start
        appointments = Appointment.objects.filter(start__gte=current_datetime, start__lte=end_date)
        return appointments

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = Doctor.objects.all()
        context['clinics'] = Clinic.objects.all()
        return context


class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_update.html'  # Предположим, что у вас есть шаблон appointment_update.html

    def get_success_url(self):
        # Перенаправление после успешного обновления записи
        return reverse('appointment_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['services_added'] = list(context['appointment'].services.all())
        return context


class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_update.html'  # Предположим, что у вас есть шаблон appointment_update.html

    def get_success_url(self):
        # Перенаправление после успешного обновления записи
        return reverse('appointment_detail', kwargs={'pk': self.object.pk})


class AppointmentDitail(DetailView):
    model = Appointment
    template_name = 'appointment_detail.html'
    context_object_name = 'appointment'
    slug_url_kwarg = 'app_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = context['appointment']
        context['services'] = appointment.services.all()
        context['sum_services'] = sum([service.cost for service in context['services']])
        return context

    def get_object(self, queryset=None):
        appointment = get_object_or_404(Appointment, pk=self.kwargs['app_id'])
        return appointment

