from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from business.models import Business_owner

""" View that returns the business owners count"""


class Business_count(APIView):
    """ Returns an int of the total number of business owners 
    """
    permission_classes = [IsAdminUser,]
    def get(self, request, *args, **kwargs):
        # Returns the count of only the business owners
        counts = Business_owner.objects.all().count()

        return Response(counts, status=status.HTTP_200_OK)
