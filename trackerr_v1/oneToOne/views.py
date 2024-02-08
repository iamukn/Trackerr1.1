from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializer import ( DepartmentSerializer, EmployeeSerializer, SpeciesSerializer)
from .models import Employee, Department, Species

class Dept_Reg(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)
        return Response(serializer.data, status='200')



class Species_get(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        species = Species.objects.all()
        serializer = SpeciesSerializer(species, many=True)

        return Response(serializer.data, status='200')
