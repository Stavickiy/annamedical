from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Doctor, Patient


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'specialization', 'doctor_photo')
    list_display_links = ('id', 'last_name')
    fields = ('first_name', 'last_name', 'doctor_photo', 'specialization', 'photo')
    readonly_fields = ['doctor_photo']

    @admin.display(description='Фото доктора')
    def doctor_photo(self, doctor: Doctor):
        return mark_safe(
            f"<a href='{doctor.photo.url}'><img src='{doctor.photo.url}' alt='{doctor.last_name}' width='100'></a>")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'doctor', 'phone_number', 'photo_display')
    list_display_links = ('id', 'last_name')
    fields = ('first_name', 'last_name', 'date_of_birth', 'doctor', 'gender',
              'phone_number', 'photo_display', 'medical_history')
    readonly_fields = ['photo_display']


    @admin.display(description='Фото пациента')
    def photo_display(self, patient: Patient):
        return mark_safe(
            f"<a href='{patient.photo.url}'><img src='{patient.photo.url}' alt='{patient.last_name}' width='100'></a>")
