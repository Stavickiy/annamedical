from django.contrib import admin
from django.utils.safestring import mark_safe

from appointment.models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'start', 'end', 'type', 'status')
    list_display_links = ('id', 'patient')
    fields = ('patient', 'doctor', 'start', 'end', 'services',
              'description', 'type', 'status', 'get_procedures')
    filter_horizontal = ('services',)
    readonly_fields = ['get_procedures']
    list_editable = ('type', 'status')

    def get_procedures(self, obj):
        return mark_safe("<br>".join([f'{p.name} {p.cost}р.' for p in obj.procedures.all()]))

    get_procedures.short_description = 'Procedures'

