from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from logistics.models import Logistics_partner

""" View that returns the logistics owners count"""


class Logistics_owners_count(APIView):
    permission_classes = [IsAdminUser,]
    def get(self, request, *args, **kwargs):
        # Returns the count of only the business owners
        counts = Logistics_partner.objects.all().count()

        return Response(counts, status=status.HTTP_200_OK)
