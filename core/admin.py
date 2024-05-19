from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Doctor, Patient, Service, Clinic


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'specialization', 'is_main', 'doctor_photo')
    list_display_links = ('id', 'last_name')
    fields = ('first_name', 'last_name', 'is_main', 'doctor_photo', 'clinic', 'specialization', 'photo')
    readonly_fields = ['doctor_photo']

    @admin.display(description='Фото доктора')
    def doctor_photo(self, doctor: Doctor):
        return mark_safe(
            f"<a href='{doctor.photo.url}'><img src='{doctor.photo.url}' alt='{doctor.last_name}' width='100'></a>")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'doctor', 'clinic', 'city',
                    'phone_number', 'instagram', 'telegram', 'photo_display',)
    list_display_links = ('id', 'last_name')
    fields = ('first_name', 'last_name', 'date_of_birth', 'doctor', 'clinic', 'city', 'gender', 'photo',
              'phone_number', 'instagram', 'telegram', 'photo_display', 'medical_history')
    readonly_fields = ['photo_display']


    @admin.display(description='Фото пациента')
    def photo_display(self, patient: Patient):
        return mark_safe(
            f"<a href='{patient.photo.url}'><img src='{patient.photo.url}' alt='{patient.last_name}' width='100'></a>")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cost')
    list_display_links = ('id', 'name')
    fields = ('name', 'cost')

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    fields = ('name',)
