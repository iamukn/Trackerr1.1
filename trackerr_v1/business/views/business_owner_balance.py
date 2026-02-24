#!/usr/bin/python3
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from .business_owner_permission import IsBusinessOwner
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from user.models import User

class Business_ownerBalance(APIView):
    """
    View that handles READ UPDATE operation on the balance
    """
    def query_set(self,instance, id, *args, **kwargs):
        # Get the user object or return a 404
        user = get_object_or_404(instance, pk=id)
        # return user a 404
        return user

    permission_classes = [IsBusinessOwner,]

    # swagger documentation
    @swagger_auto_schema(
        operation_summary="Retrieve Account Balance information of a Business Owner",
        operation_description="GET endpoint that retrieves account balance information of a business owner",
        tags=['Business Owners'],
        responses = {
            "200": openapi.Response(
            description="GETs the account balance of a business owner",
            schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "msg": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="response status",
                    ),
                "balance": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='balance in figures'
                    ),
                'symbol': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='symbol of the currency'
                    ),
                'currency': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='currency name'
                    )
                },
            example={
                'msg': 'success',
                'balance': '13',
                'symbol': '₵',
                'currency': 'GHS'
                }
            )
            ),
            '400': openapi.Response(
                description='Bad Request',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'details': openapi.Schema(type=openapi.TYPE_STRING, description='error accessing users wallet, contact admin')
                        }
                    )
                )
            ,
            "401": openapi.Response(
                description="Error: Unauthorized",
                schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Authentication credentials were not provided.")
                }
                )
                ),
            "403": openapi.Response(
                description="Error: Forbidden",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="forbidden")
                        }
                    )
                )
            }
                )
    # Get a business users data
    def get(self, request, *args, **kwargs):
        owner = request.user
        country = owner.country
        try:
            balance = format(owner.wallet.balance, '.2f')

            if country.lower() == 'nigeria': 
                # handles the balance if it's nigeria
                return Response({'msg': 'success',
                        'balance': balance,
                        'symbol': '₦',
                        'currency': 'NGN',
                    }, status=status.HTTP_200_OK)
            # handles if it's ghana; tweak for other countries as we expand
            return Response({'msg': 'success',
                    'balance': balance,
                    'symbol': '₵',
                    'currency': 'GHS',
                    }, status=status.HTTP_200_OK)

        except User.wallet.RelatedObjectDoesNotExist:
            return Response({'error': 'user does not have a wallet, contact admin'}, status=status.HTTP_400_BAD_REQUEST)
