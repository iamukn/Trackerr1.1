from affiliate.models import Affiliate, AffiliateOTP
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from affiliate.security import generate_otp, hash_otp
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
from shared.celery_tasks.utils_tasks.reusable_email_sender import send_email
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RequestOTP(APIView):

    permission_classes = [AllowAny,]

    # swagger documentation for the patch route
    @swagger_auto_schema(
        operation_description='Generates and sends an OTP to a register affiliate email!',
        operation_summary='Request Login OTP',
        tags=['Affiliate'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email':openapi.Schema(type=openapi.TYPE_STRING, description='johndoe@example.com'),
                },
            example={
                'email': 'johndoe@example.com',
                }
            ),
        responses = {
            '200': openapi.Response(
                description='Otp Sent Successfully',
                schema = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'msg': openapi.Schema(type=openapi.TYPE_STRING, description='OTP success message'),
                    }
                ),
                example={
                    "msg": "an otp has been sent to your email"
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
                ),
            '429': openapi.Response(
                    description='Error: Too Many Requests',
                    schema = openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'error': openapi.Schema(type=openapi.TYPE_INTEGER, description='too many requests')
                             },
                        example={
                            'msg': 'An OTP has already been sent. Please wait for it to expire.'
                            }
                        ))
            })

    def post(self, request):

        email = request.data.get('email')

        if email:
            # check if the email exist in db
            email = email.strip()
            affiliate_exist = Affiliate.objects.filter(email=email)
            if not affiliate_exist:
                return Response({'msg': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)

            affiliate = affiliate_exist [0]
            now = timezone.now()
            try:
                # store otp has and send otp via email
                existing_otp = AffiliateOTP.objects.filter(
                    affiliate=affiliate,
                    is_used=False,
                    expires_at__gt=now,
                ).exists()

                if existing_otp:
                 raise ValidationError(
                    "An OTP has already been sent. Please wait for it to expire."
                )
                # generate otp
                otp = generate_otp()
                # create otp record
                AffiliateOTP.objects.create(
                    affiliate=affiliate,
                    otp_hash=hash_otp(affiliate.email, otp),
                    expires_at=now + timedelta(minutes=10),
                )
                # send otp via email
                subject = "TrackerrGo OTP"
                message = "Your Login OTP is {} and it expires in 5 minutes.".format(otp)
            
                send_email.apply_async(
                    kwargs={"subject": subject, "email": affiliate.email, "message": message}
                        )
                return Response({'msg':'an otp has been sent to your email'}, status=status.HTTP_200_OK)
            except ValidationError:
                return Response({'msg': 'An OTP has already been sent. Please wait for it to expire.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            except Exception as e:
                return Response({'msg': {'error': {'server_error': ['an internal server error occurred!']}}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': {'error':{'email_error': ['email is required!']}}}, status=status.HTTP_400_BAD_REQUEST)
