#!/usr/bin/python3
from django.contrib.auth.hashers import check_password, make_password

""" GET OTP Owner """

def get_otp_or_none(otp, model):
    otp = str(otp)
    hash_otp = make_password(otp)
    otp_owner = model.objects.all()
    for otps in otp_owner:
        # check if a hash password exist
        if otps.hashed_otp:
            # check if it matches what is in the database
            if check_password(otp, otps.hashed_otp):
                return otps
    return None
