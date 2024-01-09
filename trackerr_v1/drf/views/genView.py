from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from drf.serializer import UsersSerializer
from rest_framework.response import Response

class GenView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UsersSerializer

    def list(self, request):

        query = self.get_queryset()

        serializer = UsersSerializer(query, many=True)
        return Response(serializer.data)
