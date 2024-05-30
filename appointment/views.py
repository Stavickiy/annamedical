from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, TemplateView, FormView

from appointment.forms import AppointmentItemFormSet
from appointment.models import Appointment, AppointmentStatus, AppointmentType
from core.models import Service, Doctor, Clinic, Patient
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse, reverse_lazy


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


class CreateAppointmentVew(TemplateView):
    template_name = 'new/create_appointment.html'
    extra_context = {'title': 'Запись пациента на прием'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = Doctor.objects.all()
        context['clinics'] = Clinic.objects.all()
        patient = get_object_or_404(Patient, pk=self.request.GET.get('patient_id'))
        context['patient'] = patient
        context['patients'] = Patient.objects.all().exclude(pk=self.request.GET.get('patient_id'))
        context['statuses'] = AppointmentStatus.choices
        context['types'] = AppointmentType.choices
        context['services'] = Service.objects.all()
        return context


# class AppointmentUpdateView(UpdateView):
#     model = Appointment
#     form_class = AppointmentForm
#     template_name = 'appointment_update.html'
#
#     def get_success_url(self):
#         # Перенаправление после успешного обновления записи
#         return reverse('appointment_detail', kwargs={'pk': self.object.pk})
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['services'] = Service.objects.all()
#         context['services_added'] = list(context['appointment'].services.all())
#         return context


class AppointmentDitail(DetailView):
    model = Appointment
    template_name = 'new/appointment_detail.html'
    context_object_name = 'appointment'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = self.get_object()
        context['doctors'] = Doctor.objects.all()
        context['clinics'] = Clinic.objects.all()
        context['statuses'] = AppointmentStatus.choices
        context['types'] = AppointmentType.choices
        context['items'] = appointment.items.all()
        context['services_selected'] = [item.service for item in context['items']]
        context['services'] = Service.objects.all()
        context['sum_services'] = sum([item.price * item.quantity for item in context['items']])
        context['patients'] = Patient.objects.all()

        # Создание formset и добавление его в контекст
        if self.request.POST:
            context['formset'] = AppointmentItemFormSet(self.request.POST, instance=appointment)
        else:
            context['formset'] = AppointmentItemFormSet(instance=appointment)

        return context

class UpdateAppointmentItemsView(FormView):
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

