from rest_framework import serializers

from appointment.models import Appointment, AppointmentItem, Media
from core.models import Patient, Service
from django.urls import reverse


class PatientSerializer(serializers.ModelSerializer):
    doctor_full_name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    clinic_name = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = (
            'id', 'first_name', 'last_name', 'full_name', 'photo', 'date_of_birth', 'phone_number', 'medical_history',
            'doctor_full_name', 'doctor', 'url', 'clinic_name')

    def get_doctor_full_name(self, obj):
        return obj.doctor.full_name()

    def get_url(self, obj):
        return reverse('core:patient_detail', kwargs={'pk': obj.id})

    def get_clinic_name(self, obj):
        return obj.clinic.name


class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id',
            'first_name',
            'last_name',
            'date_of_birth',
            'doctor',
            'phone_number',
            'medical_history',
            'photo',
            'city',
            'clinic',
            'instagram',
            'telegram'
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_full_name = serializers.SerializerMethodField()
    patient_full_name = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    clinic_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ('id', 'start_date', 'start_time', 'end_time', 'patient_full_name',
                  'doctor_full_name', 'get_status_display', 'description', 'status', 'url', 'clinic_name')

    def get_doctor_full_name(self, obj):
        return obj.doctor.full_name()

    def get_patient_full_name(self, obj):
        return obj.patient.full_name()

    def get_start_time(self, obj):
        return obj.start.time().strftime('%H:%M')

    def get_end_time(self, obj):
        return obj.end.time().strftime('%H:%M')

    def get_start_date(self, obj):
        return obj.start.date().strftime('%d %B %Y г.')

    def get_url(self, obj):
        return reverse('appointment:appointment_detail', kwargs={'app_id': obj.id})

    def get_clinic_name(self, obj):
        return obj.clinic.name


class AppointmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentItem
        fields = '__all__'


class AppointmentDetailSerializer(serializers.ModelSerializer):
    items = AppointmentItemSerializer(many=True, required=False)

    class Meta:
        model = Appointment
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta():
        model = Service
        fields = '__all__'


class AppointmentMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
