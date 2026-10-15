from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from affiliate.serializer import AffiliateSerializer
from django.db import transaction
from affiliate.models import Affiliate
from django.db.utils import IntegrityError
from affiliate.utils.generate_referral_code import generate_referral_code
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CreateAffiliate(APIView):

    permission_classes = [AllowAny,]

    # swagger documentation for the patch route
    @swagger_auto_schema(
        operation_description='Create a new affiliate partner',
        operation_summary='Create Affiliate',
        tags=['Affiliate'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email':openapi.Schema(type=openapi.TYPE_STRING, description='johndoe@example.com'),
                'full_name':openapi.Schema(type=openapi.TYPE_STRING, description='john doe'),
                },
            example={
                'email': 'johndoe@example.com',
                'full_name': 'john doe'
                }
            ),
        responses = {
            '200': openapi.Response(
                description='Account Created Successfully',
                schema = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'msg': openapi.Schema(type=openapi.TYPE_STRING, description='Account Creation Description'),
                    }
                ),
                example={
                    "msg": "account created successfully!"
                }
                ),
            '400': openapi.Response(
                description='Bad Request',
                schema = openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'msg': openapi.Schema(type=openapi.TYPE_OBJECT,
                            properties={
                                'error': openapi.Schema(type=openapi.TYPE_OBJECT,
                                        properties={
                                            'error_key': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                items={
                                                    'error_message': openapi.Schema(type=openapi.TYPE_STRING, description="Error description")
                                                    }
                                                )
                                            }
                                    )
                                }
                            )},
                    example = {
                        'msg': {'error': {'email_error': ['email is required']}}
                        }
                    ))
            ,

            '401': openapi.Response(
                description='Error: Unauthorized',
                schema = openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_INTEGER, description='Authentication credentials were not provided.')
                        },
                example={
                    'detail': 'Authentication credentials were not provided.'
                    }
                )
            ),

            '403': openapi.Response(
                description='Error: Forbidden',
                schema = openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_INTEGER, description='forbidden')
                        },
                    example={
                        'error': 'forbidden'
                        }
                    )
                ),
            })

    def post(self, request, *arg, **kwargs):

        data = request.data

        if "email" not in data and "full_name" not in data:
            return Response({'msg': {'error':{'email_full_name_error':['email and name are required!']}}}, status=status.HTTP_400_BAD_REQUEST)

        elif "email" not in data:
            return Response({'msg': {'error': {'email_error': ['email is required!']}}}, status=status.HTTP_400_BAD_REQUEST)

        elif "full_name" not in data:
            return Response({'msg': {'error': [{'full_name_error': ['full name is required!']}]}}, status=status.HTTP_400_BAD_REQUEST)

        email = data.get('email').strip().lower()
        full_name = data.get('full_name').strip().lower()

        for _ in range(5):
            try:
                code = generate_referral_code()
                with transaction.atomic():
                    serializer = AffiliateSerializer(data={"email": email, "full_name": full_name, "referral_code": code})
                    if serializer.is_valid():
                        serializer.save()
                        # send email
                        return Response({'msg': 'account created successfully!'}, status=status.HTTP_200_OK)
                    return Response({'msg': {'error': serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                raise e
                Response({'msg': 'an internal error occurred, please try again!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
