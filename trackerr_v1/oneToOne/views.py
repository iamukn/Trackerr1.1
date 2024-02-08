from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializer import (DepartmentSerializer, EmployeeSerializer)
from .models import Employee, Department

class Dept_Reg(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        department = Department.objects.all()
        serializer = DepartmentSerializer(department, many=True)
        return Response(serializer.data, status='200')

