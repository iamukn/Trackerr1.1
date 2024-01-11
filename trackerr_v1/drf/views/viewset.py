from django.contrib.auth.models import User
from drf.serializer import UsersSerializer
from rest_framework.viewsets import ModelViewSet

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


