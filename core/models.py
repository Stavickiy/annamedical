from PIL import Image, ExifTags
from io import BytesIO
import sys

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=30, default='')
    is_main = models.BooleanField(default=False, blank=True)
    photo = models.ImageField(upload_to='doctors_photo/')
    specialization = models.CharField(max_length=200, default=0)
    clinic = models.ManyToManyField(Clinic, related_name='doctors', blank=True)

    def full_name(self):
        return ' '.join((str(self.last_name), str(self.first_name)))

    def __str__(self):
        return ' '.join((str(self.last_name), str(self.first_name)))


class GenderType(models.TextChoices):
    FEMALE = 'female', 'Женский'
    MALE = 'male', 'Мужской'


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='patients')
    phone_number = models.CharField(max_length=20)
    medical_history = models.TextField(blank=True)
    photo = models.ImageField(upload_to='patients_photo/', blank=True)
    city = models.CharField(max_length=100, blank=True, default=0)
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT, related_name='patients', default=None, null=True)
    instagram = models.CharField(max_length=100, blank=True)
    telegram = models.CharField(max_length=100, blank=True)

    class Meta():
        ordering = ['last_name', 'first_name']


    def __str__(self):
        return ' '.join((str(self.last_name), str(self.first_name)))

    def full_name(self):
        return ' '.join((str(self.last_name), str(self.first_name)))

    def birthday(self):
        if self.date_of_birth:
            return self.date_of_birth.strftime('%Y-%m-%d')
        else:
            return None


class Service(models.Model):
    name = models.CharField(max_length=100)
    cost = models.IntegerField(default=0)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
