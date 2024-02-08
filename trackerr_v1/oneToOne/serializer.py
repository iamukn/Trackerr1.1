from .models import (Department, Employee)
from rest_framework.serializers import ModelSerializer

class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        depth = 1


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        depth = 1
