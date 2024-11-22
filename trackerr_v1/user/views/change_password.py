#!/usr/bin/python3
from rest_framework.response import Response
from .password_permission import IsBusinessOrLogisticsOwner
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from shared.celery_tasks.auth_tasks.send_email import send_update_email
from shared.logger import setUp_logger
from .password_recovery import Recover_password
from django.shortcuts import get_object_or_404
from user.utils.shortcuts import get_otp_or_none
from django.db import transaction
from user.models import Otp

# logger
logger = setUp_logger(__name__, 'business.logs')

""" Change Password Feature """

class ChangePassword(Recover_password):
    ''' Route for password change for authenticated users '''
    permission_classes = [IsBusinessOrLogisticsOwner,]

    def post(self, request, *args, **kwargs):
        # Receives a post request from Logged in user for password change
        email = request.user.email
        user = self.get_queryset(email)
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
       
        if user:
            if password1 == password2:
                with transaction.atomic():
                    user.set_password(password1)
                    user.save()
                    return Response(status=status.HTTP_206_PARTIAL_CONTENT)
            return Response({"error": "passwords must match"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": f"{email} not found"},status=status.HTTP_400_BAD_REQUEST)

class UpdatePassword(Recover_password):
    """ Route for password change for reset password endpoints """
    
    permission_classes = [AllowAny,]
    # handles the post request
    def post(self, request, *args, **kwargs):
        # retrieve data from the request object
        otp = request.data.get('otp')
        #email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        # get user
        #user = self.get_queryset(email)
        # get otp owner
        otp_owner = get_otp_or_none(otp=otp, model=Otp)

        if otp_owner:
            if password1 != password2:
                return Response({"error": "password must match!"}, status=status.HTTP_400_BAD_REQUEST)
            user_otp = otp_owner
            # check if the otp is still valid
            if user_otp.hashed_otp == None:
                return Response({"error": "otp doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            if user_otp.check_otp(otp=str(otp)):
                with transaction.atomic():
                    # set password
                    user = user_otp.owner
                    user.set_password(password1)
                    user.save()
                    # reset the otp
                    user_otp.hashed_otp = None
                    user_otp.save()
                    #send update email
                    try:
                        send_update_email.delay(email=user.email, name=user.name)
                    except Exception as e:
                        logger.error(f"Failed to enqueue email task: {str(e)}")
                    return Response({"message":"password updated successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "incorrect or expired otp"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": f"otp does not exist"}, status=status.HTTP_404_NOT_FOUND)
