from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializer import (DepartmentSerializer, EmployeeSerializer)


class Dept_Reg(APIView):
    permission_classes = [AllowAny]

    def get(self):
        return Response('Hello From Dept_REGAPI')

