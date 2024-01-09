from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from drf.serializer import UsersSerializer

class GenView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UsersSerializer
