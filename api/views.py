from django.shortcuts import render, get_object_or_404

from rest_framework import generics, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serialisers import PatientSerializer
from core.models import Patient, Doctor


class PatientsViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientsAPIList(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DoctorPatientsAPIList(ListAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        doctor_pk = self.kwargs['pk']
        doctor = get_object_or_404(Doctor, pk=doctor_pk)
        patients = doctor.patients.all()
        return patients
