from django.contrib import admin
from .models import Department, Employee,Specie, Species, Animal
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Species)
admin.site.register(Animal)
admin.site.register(Specie)
# Register your models here.
