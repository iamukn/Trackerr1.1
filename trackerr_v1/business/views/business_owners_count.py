from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from business.models import Business_owner
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

""" View that returns the business owners count"""


class Business_count(APIView):
    """ 
        Returns an integer of the total number of business owners 
        HTTP Method allowed - GET


    """
    permission_classes = [IsAdminUser,]
    # swagger documentation
    @swagger_auto_schema(operation_description="GET the total of all business owners. \n Open to only admin users only", 
            operation_summary="Retrieves count of all business owners",
            tags=['Business Owner'],
            responses={
                200: openapi.Response(
                     description="Successful",
                     schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "count": openapi.Schema(type=openapi.TYPE_NUMBER, example=5)
                            }
                         )
                    ),
                403: openapi.Response(
                    description='Error: Forbidden',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties= {
                            "detail": openapi.Schema(type=openapi.TYPE_STRING, example='forbidden')
                            }
                    )
                    ),
                401: openapi.Response(
                    description='Error: Unauthorized',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties= {
                            "detail": openapi.Schema(type=openapi.TYPE_STRING, example='Authentication credentials were not provided.')
                            }
                        )
                    )
                }
            )
    def get(self, request, *args, **kwargs):
        # Returns the count of only the business owners
        counts = Business_owner.objects.all().count()

        return Response(counts, status=status.HTTP_200_OK)
