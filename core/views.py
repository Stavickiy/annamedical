from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_date
from django.views.generic import ListView, TemplateView, DetailView
from django.utils import timezone
from datetime import datetime, timedelta, time

from appointment.models import Appointment
from users.models import User
from .mixins import ClinicAccessMixin
from .models import Doctor, Patient, Clinic, Service


class IndexPage(LoginRequiredMixin, TemplateView):
    template_name = 'new/index.html'
    extra_context = {'title': 'Менеджмент пациентов'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # получаем id клиник в которых работает доктор(user)
        user = self.request.user
        clinics_ids = Doctor.objects.get(id=user.doctor.id).clinic.values_list('id', flat=True)

        context['doctors'] = set([doctor for clinic in user.doctor.clinic.all() for doctor in clinic.doctors.all()])
        context['clinics'] = user.doctor.clinic.all()

        # Получение параметров фильтрации
        doctor_id = self.request.GET.get('doctor_id')
        clinic_id = self.request.GET.get('clinic_id')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        appointments = Appointment.objects.filter(clinic__id__in=clinics_ids)

        if start_date:
            start_date_parsed = datetime.combine(parse_date(start_date), time.min)
            appointments = appointments.filter(start__gte=start_date_parsed)
            context['start_date'] = start_date

        if end_date:
            end_date_parsed = datetime.combine(parse_date(end_date), time.max)
            appointments = appointments.filter(start__lte=end_date_parsed)
            context['end_date'] = end_date

        if not start_date and not end_date:
            # Получаем текущую дату без учета времени
            current_date = datetime.now().date()
            end_date = current_date + timedelta(days=7)
            context['start_date'] = current_date.strftime('%Y-%m-%d')
            context['end_date'] = end_date.strftime('%Y-%m-%d')

            # Фильтруем записи Appointment по полю start и клинике доктора
            appointments = appointments.filter(
                start__gte=datetime.combine(current_date, time.min),
                start__lte=datetime.combine(end_date, time.max),
                clinic__id__in=clinics_ids
            )

        if doctor_id and doctor_id != 'Доктор':
            context['doctor_selected'] = get_object_or_404(Doctor, id=doctor_id)
            appointments = appointments.filter(doctor_id=doctor_id)
        else:
            context['doctor_selected'] = None

        if clinic_id and clinic_id != 'Клиника':
            context['clinic_selected'] = get_object_or_404(Clinic, id=clinic_id)
            appointments = appointments.filter(clinic_id=clinic_id)
        else:
            context['clinic_selected'] = None

        context['appointments'] = appointments
        return context


class PatientsPage(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'new/patients.html'
    context_object_name = 'patients'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Получение параметров фильтрации
        doctor_id = self.request.GET.get('doctor_id')
        clinic_id = self.request.GET.get('clinic_id')

        if doctor_id and doctor_id != 'Доктор':
            context['doctor_selected'] = get_object_or_404(Doctor, id=doctor_id)
        else:
            context['doctor_selected'] = None

        if clinic_id and clinic_id != 'Клиника':
            context['clinic_selected'] = get_object_or_404(Clinic, id=clinic_id)
        else:
            context['clinic_selected'] = None

        context['doctors'] = set([doctor for clinic in user.doctor.clinic.all() for doctor in clinic.doctors.all()])
        context['clinics'] = user.doctor.clinic.all()
        return context

    def get_queryset(self):
        user = self.request.user
        clinics_ids = Doctor.objects.get(id=user.doctor.id).clinic.values_list('id', flat=True)

        patients = Patient.objects.filter(clinic__id__in=clinics_ids)

        # Получение параметров фильтрации
        doctor_id = self.request.GET.get('doctor_id')
        clinic_id = self.request.GET.get('clinic_id')

        # Фильтрация по доктору, если передан doctor_id
        if doctor_id and doctor_id != 'Доктор':
            patients = patients.filter(doctor_id=doctor_id)

        # Фильтрация по клинике, если передан clinic_id
        if clinic_id and clinic_id != 'Клиника':
            patients = patients.filter(clinic_id=clinic_id)
        return patients


class PatientDetail(LoginRequiredMixin, ClinicAccessMixin, DetailView):
    model = Patient
    template_name = 'new/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = context['patient']

        context['appointments'] = list(patient.appointments.all().prefetch_related('media').order_by('-start'))

        # выбираем только тех докторов которы работают в клиниках юзера
        user = self.request.user
        context['doctors'] = set([doctor for clinic in user.doctor.clinic.all() for doctor in clinic.doctors.all()])
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
                                                             doctor=user.doctor)
        context['patients'] = Patient.objects.filter(doctor=user.doctor)
        return context

class AddPatientView(TemplateView):
    template_name = 'new/add_patient.html'
    extra_context = {'title': 'Добавление пациента'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = Doctor.objects.all()
        context['clinics'] = Clinic.objects.all()
        return context

class ServicesView(ListView):
    template_name = 'new/services.html'
    model = Service
    context_object_name = 'services'


def custom_page_not_found_view(request, exception):
    return render(request, 'new/error-404.html', {'title': 'Страница не найдена'}, status=404)
