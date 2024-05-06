from django.db import models

class Doctor(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    is_main = models.BooleanField(default=False, blank=True)
    photo = models.ImageField(upload_to='doctors_photo/')
    specialization = models.CharField(max_length=200, default=0)

    def full_name(self):
        return ' '.join((str(self.last_name), str(self.first_name)))

    def __str__(self):
        return ' '.join((str(self.last_name), str(self.first_name)))


class GenderType(models.TextChoices):
    FEMALE = 'female', 'Женский'
    MALE = 'male', 'Мужской'


class Clinic(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='patients')
    gender = models.CharField(max_length=20, choices=GenderType.choices)
    phone_number = models.CharField(max_length=20)
    medical_history = models.TextField(blank=True)
    photo = models.ImageField(upload_to='patients_photo/', blank=True)
    city = models.CharField(max_length=100, blank=True, default=0)
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT, related_name='patients', default=None, null=True)
    instagram = models.CharField(max_length=100, blank=True)
    telegram = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return ' '.join((str(self.last_name), str(self.first_name)))

    def full_name(self):
        return ' '.join((str(self.last_name), str(self.first_name)))


class Service(models.Model):
    name = models.CharField(max_length=100)
    cost = models.IntegerField(default=0)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
