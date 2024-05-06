from django import forms
from .models import Appointment

from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['start', 'end', 'patient', 'doctor', 'type', 'status', 'description', 'services']
        widgets = {
            'start': forms.DateTimeInput(attrs={'class': 'form-control bg-light border-0 datetimepicker-input', 'placeholder': 'Appointment Start Time', 'data-target': '#date1', 'data-toggle': 'datetimepicker'}),
            'end': forms.DateTimeInput(attrs={'class': 'form-control bg-light border-0 datetimepicker-input', 'placeholder': 'Appointment End Time', 'data-target': '#date1', 'data-toggle': 'datetimepicker'}),
            'patient': forms.Select(attrs={'class': 'form-select bg-light border-0', 'style': 'height: 55px;'}),
            'doctor': forms.Select(attrs={'class': 'form-select bg-light border-0', 'style': 'height: 55px;'}),
            'type': forms.Select(attrs={'class': 'form-control bg-light border-0', 'placeholder': 'Appointment Type', 'style': 'height: 55px;'}),
            'status': forms.Select(attrs={'class': 'form-control bg-light border-0', 'placeholder': 'Status', 'style': 'height: 55px;'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-light border-0', 'placeholder': 'Description', 'style': 'height: 55px;'}),
            'services': forms.CheckboxSelectMultiple(attrs={'class': 'form-check'})
        }

