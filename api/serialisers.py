from rest_framework import serializers

from core.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    doctor_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ('id','first_name', 'last_name', 'full_name', 'photo', 'date_of_birth',
                  'gender', 'phone_number', 'medical_history', 'doctor_full_name', 'doctor')

    def get_doctor_full_name(self, obj):
        return f"{obj.doctor.last_name} {obj.doctor.first_name}"
