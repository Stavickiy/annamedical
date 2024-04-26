from django.db import models

class Doctor(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    is_main = models.BooleanField(default=False, blank=True)
    photo = models.ImageField(upload_to='doctors_photo/')
    specialization = models.CharField(max_length=200, default=0)

    def full_name(self):
        return ' '.join((str(self.first_name), str(self.last_name)))

    def __str__(self):
        return ' '.join((str(self.first_name), str(self.last_name)))


class GenderType(models.TextChoices):
    FEMALE = 'female', 'женский'
    MALE = 'male', 'мужской'


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='patients')
    gender = models.CharField(max_length=20, choices=GenderType.choices)
    phone_number = models.CharField(max_length=20)
    medical_history = models.TextField(blank=True)
    photo = models.ImageField(upload_to='patients_photo/', blank=True)
