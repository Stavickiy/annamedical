from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from appointment.models import Appointment
from core.models import Service


class Appointments(ListView):
    model = Appointment
    template_name = 'appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        appointments = Appointment.objects.all()
        return appointments

class AppointmentDitail(DetailView):
    model = Appointment
    template_name = 'appointment_detail.html'
    context_object_name = 'appointment'
    slug_url_kwarg = 'app_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = context['appointment']
        context['services'] = appointment.services
        return context

    def get_object(self, queryset=None):
        appointment = get_object_or_404(Appointment, pk=self.kwargs['app_id'])
        return appointment
