from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, TemplateView, FormView

from appointment.forms import AppointmentItemFormSet
from appointment.models import Appointment, AppointmentStatus, AppointmentType
from core.mixins import ClinicAppointmentAccessMixin
from core.models import Service, Doctor, Clinic, Patient
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse, reverse_lazy


class CreateAppointmentVew(LoginRequiredMixin, TemplateView):
    template_name = 'new/create_appointment.html'
    extra_context = {'title': 'Запись пациента на прием'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # выбираем только тех докторов которы работают в клиниках юзера
        context['doctors'] = set([doctor for clinic in user.doctor.clinic.all() for doctor in clinic.doctors.all()])

        # выбираем только те клиники в которых работает юзер
        context['clinics'] = user.doctor.clinic.all()
        patient = get_object_or_404(Patient, pk=self.request.GET.get('patient_id'))
        context['patient_selected'] = patient

        # выбираем только тех пациентов которые относятся к клиникам юзера
        context['patients'] = set([patient for clinic in user.doctor.clinic.all() for patient in clinic.patients.all()])

        context['statuses'] = AppointmentStatus.choices
        context['types'] = AppointmentType.choices
        context['services'] = Service.objects.all()
        return context


class AppointmentDitail(LoginRequiredMixin, ClinicAppointmentAccessMixin, DetailView):
    model = Appointment
    template_name = 'new/appointment_detail.html'
    context_object_name = 'appointment'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        appointment = self.get_object()

        # выбираем только тех докторов которы работают в клиниках юзера
        context['doctors'] = set([doctor for clinic in user.doctor.clinic.all() for doctor in clinic.doctors.all()])

        # выбираем только те клиники в которых работает юзер
        context['clinics'] = user.doctor.clinic.all()

        # выбираем только тех пациентов которые относятся к клиникам юзера
        context['patients'] = set([patient for clinic in user.doctor.clinic.all() for patient in clinic.patients.all()])

        context['statuses'] = AppointmentStatus.choices
        context['types'] = AppointmentType.choices
        context['items'] = appointment.items.all()
        context['services_selected'] = [item.service for item in context['items']]
        context['services'] = Service.objects.all()
        context['sum_services'] = sum([item.price * item.quantity for item in context['items']])


        # Создание formset и добавление его в контекст
        if self.request.POST:
            context['formset'] = AppointmentItemFormSet(self.request.POST, instance=appointment)
        else:
            context['formset'] = AppointmentItemFormSet(instance=appointment)

        return context

class UpdateAppointmentItemsView(LoginRequiredMixin, ClinicAppointmentAccessMixin,  FormView):
    form_class = AppointmentItemFormSet
    template_name = 'new/appointment_detail.html'

    def get_success_url(self):
        return reverse_lazy('appointment_detail', kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        appointment = get_object_or_404(Appointment, pk=self.kwargs['pk'])
        kwargs['instance'] = appointment
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

