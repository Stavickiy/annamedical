from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import Doctor


class User(AbstractUser):
    phone_number = models.CharField(blank=True, default=0, max_length=12)
    doctor = models.OneToOneField(to=Doctor, on_delete=models.PROTECT, default=None, null=True)
