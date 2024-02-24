from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from logistics.models import Logistics_partner

""" View that returns the business owners count"""


class Business_count(APIView):

    def get(self, request, *args, **kwargs):
        # Returns the count of only the business owners
        counts = Logistics_partner.objects.all().count()

        return Response(counts, status=status.HTTP_200_OK)
