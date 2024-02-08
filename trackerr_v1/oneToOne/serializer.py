from .models import (Department, Employee, Species)
from rest_framework.serializers import ModelSerializer

class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        depth = 0


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        depth = 0


class SpeciesSerializer(ModelSerializer):
    class Meta:
        model = Species
        fields = '__all__'
        depth = 1
