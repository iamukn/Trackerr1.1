from rest_framework.response import Response
from user.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

""" View that returns the count of all users """

class Users_count(APIView):
    """ Fetches the count of all the users"""
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs) -> int:
        # fetches the user and returns its count

        count = User.objects.values('email').count()
        return Response(count, status=status.HTTP_200_OK)
