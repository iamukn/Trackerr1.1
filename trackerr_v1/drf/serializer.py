from rest_framework.serializers import ModelSerializer
from .models import Books
from django.contrib.auth.models import User

class BookSerializer(ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'
        depth = 1

class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']
