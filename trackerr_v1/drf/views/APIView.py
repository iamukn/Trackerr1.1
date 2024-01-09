from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import authentication, permissions

class ListView(APIView):
    """ This view will list all users in the system """
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def get(self, request, format=None, *args, **kwargs):
        user = [(users.username, users.email) for users in User.objects.all()]
        return Response(user, status=200)
