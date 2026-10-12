from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from business.views.business_owner_permission import IsBusinessOwner
from affiliate.security import hash_otp, verify_otp_hash
import secrets
from user.serializers import UsersSerializer
from shared.celery_tasks.utils_tasks.reusable_email_sender import send_email
from shared.celery_tasks.utils_tasks.reusable_sms import reusable_sms_sender as send_sms

def otp_gen():
    return f"{secrets.randbelow(10_000):04d}"

class SendVerificationCode(APIView):

    permission_classes = [IsBusinessOwner,]

    def post(self, request):

        try:
            channel = request.data.get('channel')

            if channel in ['phone', 'email']:

                otp = otp_gen()
                user = request.user
                email = user.email
                phone = user.phone_number

                hashed_otp = hash_otp(email=email, otp=otp)
                # store hashed in the db
                if hashed_otp:
                    if channel == 'email':
                        serializer = UsersSerializer(user, data={'email_verify_hash': hashed_otp}, partial=True)
                    elif channel == 'phone':
                        serializer = UsersSerializer(user, data={'phone_verify_hash': hashed_otp}, partial=True)

                if serializer.is_valid():
                    serializer.save()

                    if channel == 'email':
                        # send the otp via email
                        subject = 'TrackerrGo Email Verification Code'
                        message = f"Your TackerrGo Business Account Email Verification OTP is {otp}"
                        send_email.apply_async(
                            kwargs={'subject': subject, 'email': email, 'message': message}
                                )
                        return Response({'msg': 'email sent successfully'}, status=status.HTTP_200_OK)
                    elif channel == 'phone':
                        if phone:
                            if (len(phone) == 11):
                                phone = f"{phone[1:]}"
                            elif (len(phone) == 10):
                                phone = phone
                            phone = f"234{phone.strip()}"
                            # send sms
                            country = user.country
                            message = f"TrackerrGo OTP: Your phone number verification code is {otp}"

                            send_sms.apply_async(
                                kwargs={'country': country, 'phone': phone, 'message': message}
                                    )
                            return Response({'msg': 'sms sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'an internal server error occurred!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyAccount(APIView):

    permission_classes = [IsBusinessOwner,]

    def post(self, request):

        data = request.data
        user = request.user
        
        email = user.email
        #get the phone and email code
        phone_otp = data.get('phoneCode')
        email_otp = data.get('emailCode')
        # verify against stored hash
        stored_phone_hash = user.phone_verify_hash
        stored_email_hash = user.email_verify_hash
    
        email_hash_verified = verify_otp_hash(email, email_otp, stored_email_hash)
        phone_hash_verified = verify_otp_hash(email, phone_otp, stored_phone_hash)

        if not email_hash_verified and not phone_hash_verified:
            return Response({'msg': 'Email and phone otp are invalid'}, status=status.HTTP_400_BAD_REQUEST)
        elif not email_hash_verified:
            return Response({'msg': 'Email otp is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        elif not phone_hash_verified:
            return Response({'msg': 'Phone otp is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        elif email_hash_verified and phone_hash_verified:
            # mark as verified
            serializer = UsersSerializer(user, data={"is_verified": True, "email_verified": True, "phone_verified": True}, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response({"msg": "account verification successful"},status=status.HTTP_200_OK)
