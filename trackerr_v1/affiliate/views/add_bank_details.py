from rest_framework.views import APIView
from rest_framework import status
from affiliate.serializer import AccountDetailsSerializer
from rest_framework.response import Response
from affiliate.authentication import AffiliateTokenAuthentication
from affiliate.permissions import IsAffiliate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from affiliate.utils.list_banks import list_banks
from django.core.cache import cache


class AccountDetails(APIView):
    authentication_classes = [AffiliateTokenAuthentication,]
    permission_classes = [IsAffiliate,]

    @swagger_auto_schema(
        operation_description='Adds Bank Account Information',
        operation_summary='This Endpoint Adds Bank Information To An Affialiates Account!',
        tags=['Affiliate'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'bank_name':openapi.Schema(type=openapi.TYPE_STRING, description='bank name'),
                'account_number': openapi.Schema(type=openapi.TYPE_STRING, description='bank account number'),
                },
            example={
                'bank_name': 'Access Bank',
                'account_number':'0987654562'
                }
            ),
        responses = {
            '200': openapi.Response(
                description='Account Added Successfully',
                schema = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'msg': openapi.Schema(type=openapi.TYPE_OBJECT,
                        properties = {
                            'bank_name': openapi.Schema(type=openapi.TYPE_STRING, description='bank name'),
                            'account_number': openapi.Schema(type=openapi.TYPE_STRING, description='bank account number')
                            })
                    }
                ),
                example={
                    "msg": {
                        'bank_name': 'ekondo bank',
                        'account_number': '0637282922'
                        }
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
                        'msg': {'error': {'email_error': ['email is invalid']}}
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
                )
            })

    def post(self, request):

        data = request.data

        if "bank_name" not in data and "account_number" not in data:
            return Response({"msg": { 'error': {'bank_name_and_account_error': ["bank name and account number are required!"]}}}, status=status.HTTP_400_BAD_REQUEST)

        elif "account_number" not in data:
            return Response({"msg": {'error': {'account_number_error':["account number is required!"]}}}, status=status.HTTP_400_BAD_REQUEST)

        elif "bank_name" not in data:
            return Response({"msg": {'error': {'bank_name_error': ["bank account is required!"]}}}, status=status.HTTP_400_BAD_REQUEST)


        bank_name = data.get('bank_name')
        account_number = data.get('account_number')

        serializer = AccountDetailsSerializer(data={"bank_name": bank_name, "account_number": account_number, "affiliate": request.user.id})

        if serializer.is_valid():
            serializer.save()

            data = serializer.data
            data.pop("affiliate")
            data.pop("id")

            return Response({'msg': data}, status=status.HTTP_200_OK)
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class Banks(APIView):

    authentication_classes = [AffiliateTokenAuthentication,]
    permission_classes = [IsAffiliate,]

    def get(self, request):

        banks = list_banks()

        return Response({'banks': banks}, status=status.HTTP_200_OK)

    def post(self, request):

        data = request.data
        account_number = data.get('account_number')
        bank_code = data.get('bank_code')

        if not account_number or not bank_code:
            return Response({'name': ''}, status=status.HTTP_200_OK)

        cache_key = f"{account_number}:{bank_code}"
        cached = cache.get(cache_key)

        try:
            if cached:
                return Response({'name': cached}, status=status.HTTP_200_OK)
            url="https://api.paystack.co/bank/resolve?account_number={0}&bank_code={1}".format(account_number, bank_code)
            import requests, os
            headers = {
                "Authorization": f"Bearer {os.environ.get('PAYSTACK_SECRET_KEY')}",
                "Content-Type": "application/json"
                    }
            res = requests.get(url, headers=headers)

            if res.status_code == 200:
                res_data = res.json()

                if res_data.get('status') == True:
                    name = res_data.get('data').get('account_name')
                    cache.set(cache_key, name, timeout=56000)
                    return Response({'name': name}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid account details'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'an internal error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
