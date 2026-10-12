from affiliate.authentication import AffiliateTokenAuthentication
from affiliate.permissions import IsAffiliate
from affiliate.serializer import AffiliateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetAffiliate(APIView):

    authentication_classes = [AffiliateTokenAuthentication,]
    permission_classes = [IsAffiliate,]

    @swagger_auto_schema(
        operation_description='GET information about an affiliate partner',
        operation_summary='This endpoints fetches personal information belonging to an affiliate user',
        tags=['Affiliate'],
        responses = {
            '200': openapi.Response(
                description='Referral information',
                schema = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'msg': openapi.Schema(type=openapi.TYPE_OBJECT,
                        properties={
                            "affiliate": openapi.Schema(type=openapi.TYPE_OBJECT,
                                properties={
                                    "email": openapi.Schema(type=openapi.TYPE_STRING, description='affiliate email address'),
                                    "full_name": openapi.Schema(type=openapi.TYPE_STRING, description='affiliate fullname'),
                                    "referral_code": openapi.Schema(type=openapi.TYPE_STRING, description='affiliate unique referral code'),
                                    "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, description='true or false'),
                                    "total_coins_withdrawn":  openapi.Schema(type=openapi.TYPE_INTEGER, description='total coined withdrawn by an affiliate') 
                                    })
                                }
                                )
                                
                            }),
                example={
                    "email": "johndoe@example.com",
                    "full_name": "Doe John",
                    "referral_code": "XYYST6",
                    "total_coins_withdrawn": 750,
                    "is_active": True
                    }
                ),
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

    def get(self, request):
        user = request.user

        serializer = AffiliateSerializer(user)
        data = serializer.data
        # remove fields for server only
        for key in ['id', 'created_at', 'updated_at']:
            data.pop(key)
        return Response({'msg': { "affiliate" :data}}, status=status.HTTP_200_OK)
