from django.db import models

from annamedical import settings
from core.models import Patient, Doctor, Service


class AppointmentStatus(models.TextChoices):
    PLANNED = 'planned', 'Запланировано'
    APPROVED = 'approved', 'Подтверждено'
    COMPLETED = 'completed', 'Завершено'
    CANCELED = 'canceled', 'Отменено'


class AppointmentType(models.TextChoices):
    PRIMARY = 'primary', 'Первичная'
    SECONDARY = 'secondary', 'Вторичная'


class Appointment(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='appointments')
    type = models.CharField(max_length=100, choices=AppointmentType.choices)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=AppointmentStatus.choices)
    services = models.ManyToManyField(Service, related_name='appointments', blank=True)

    class Meta:
        ordering = ['start']

    def get_url_for_api(self):

        return
