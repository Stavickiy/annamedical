from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from appointment.models import Appointment
from core.models import Service
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
