from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from affiliate.models import Affiliate, AffiliateOTP, AffiliateSession
from rest_framework.permissions import AllowAny
from django.utils import timezone
from affiliate.security import verify_otp_hash, create_affiliate_session, hash_token

from affiliate.authentication import AffiliateTokenAuthentication
from affiliate.permissions import IsAffiliate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class Login(APIView):

    permission_classes = [AllowAny,]

    @swagger_auto_schema(
        operation_description='Authenticate an affiliate partner',
        operation_summary='Affiliate Authentication',
        tags=['Affiliate'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email':openapi.Schema(type=openapi.TYPE_STRING, description='johndoe@example.com'),
                'otp':openapi.Schema(type=openapi.TYPE_STRING, description='725362'),
                },
            example={
                'email': 'johndoe@example.com',
                'otp': '637353'
                }
            ),
        responses = {
            '200': openapi.Response(
                description='Authentication Successfully',
                schema = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access Token'),
                    }
                ),
                example={
                    "token": "dfghjklkjhgfdfghj6545676545876fghnsEc"
                }
                ),
            '400': openapi.Response(
                description='Bad Request',
                schema = openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'msg': openapi.Schema(type=openapi.TYPE_STRING, description="Error description"
                            )
                        },
                    example = {
                        'msg': "email is required"
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

    def post(self, request):
        data = request.data

        if "email" not in data and "otp" not in data:
            return Response({'msg': 'email and otp is required!'}, status=status.HTTP_400_BAD_REQUEST)

        elif "otp" not in data:
            return Response({'msg': 'otp is required!'}, status=status.HTTP_400_BAD_REQUEST)

        elif "email" not in data:
            return Response({'msg': 'email is required!'}, status=status.HTTP_400_BAD_REQUEST)

        email = data.get('email').strip()
        otp = str(data.get('otp')).strip()

        affiliate_exist = Affiliate.objects.filter(email=email)

        if affiliate_exist:
            affiliate = affiliate_exist[0]

            # get otp hash
            now = timezone.now()
            otp_model = AffiliateOTP.objects.filter(
                    affiliate=affiliate,
                    is_used=False,
                    expires_at__gt=now
                    )

            if otp_model:
                stored_hash =  otp_model[0].otp_hash

                is_verified = verify_otp_hash(email=email, otp=otp, stored_hash=stored_hash)
                
                if is_verified:
                    # create a session token for him and return it
                    token = create_affiliate_session(affiliate)
                    res = Response({'access': token}, status=status.HTTP_200_OK) if token else Response({'msg': 'an internal error occurred!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    return res
                return Response('OK', status=status.HTTP_200_OK)
            return Response({'msg': 'invalid otp, please generate a new otp'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'email does not exist!'}, status=status.HTTP_404_NOT_FOUND)


class Logout(APIView):    
    authentication_classes = [AffiliateTokenAuthentication,]
    permission_classes = [IsAffiliate,]

    @swagger_auto_schema(
        operation_description='Logout an affiliate partner',
        operation_summary='Affiliate Logout',
        tags=['Affiliate'],
        responses = {
            '200': openapi.Response(
                description='Logged out Successfully',
                schema = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'msg': openapi.Schema(type=openapi.TYPE_STRING, description='Logged out message'),
                    }
                ),
                example={
                    "msg": "logged out successfully!"
                }
                ),
            '400': openapi.Response(
                description='Bad Request',
                schema = openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'msg': openapi.Schema(type=openapi.TYPE_STRING, description="Error description"
                            )
                        },
                    example = {
                        'msg': "session does not exist"
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

    def post(self, request):

        headers = request.headers
        affiliate = request.user
        
        auth_token = headers.get('Authorization').split(' ')[-1].strip() if 'Authorization' in headers else False

        if auth_token:
            from affiliate.security import hash_token
            # find a session that has its hashed version and blacklist it

            session_exist = AffiliateSession.objects.filter(
                token_hash=hash_token(auth_token),
                affiliate=affiliate
                    )
            if session_exist:
                from django.utils import timezone
                session = session_exist[0]
                # updated the revoked_at

                session.revoked_at = timezone.now()
                session.save()
                return Response({'msg': 'logged out successful'}, status=status.HTTP_200_OK)
            return Response({'msg': 'user session does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'authentication credentials were not provided'}, status=status.HTTP_400_BAD_REQUEST)
