from django import forms
from .models import Appointment, AppointmentItem

class AppointmentItemForm(forms.ModelForm):
    class Meta:
        model = AppointmentItem
        fields = ['quantity', 'price']

AppointmentItemFormSet = forms.inlineformset_factory(
    Appointment,
    AppointmentItem,
    form=AppointmentItemForm,
    extra=0,
    can_delete=False
)