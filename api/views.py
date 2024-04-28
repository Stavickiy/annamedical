from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serialisers import PatientSerializer
from core.models import Patient, Doctor


class PatientAPIList(APIView):
    def get(self, request):
        if 'doc_id' in request.query_params:
            patients = Patient.objects.filter(doctor=request.query_params['doc_id']).values()
        else:
            patients = Patient.objects.all().values()

        for patient in patients:
            patient['photo'] = '/media/' + patient['photo']
            patient['full_name'] = patient['first_name'] + ' ' + patient['last_name']
        doctor_name = get_object_or_404(Doctor, pk=patient['doctor_id']).full_name()
        patient['doctor_name'] = doctor_name
        return Response({'patients': patients})


# class PatientAPIList(generics.ListAPIView):
#     queryset = Patient.objects.all()
#     serializer_class = PatientSerializer
