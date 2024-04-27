from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from .models import Doctor, Patient


class HomePage(TemplateView):
    template_name = 'index.html'
    extra_context = {'title': 'Менеджмент пациентов'}

class DoctorsPage(ListView):
    model = Doctor
    template_name = 'doctors.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        doctors = Doctor.objects.all()
        return doctors


class ServicePage(TemplateView):
    template_name = 'services.html'
    extra_context = {'title': 'Наши услуги'}


class PatientsPage(ListView):
    model = Patient
    template_name = 'patients.html'
    context_object_name = 'patients'
