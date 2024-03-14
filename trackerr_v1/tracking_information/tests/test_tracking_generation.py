#!/usr/bin/python3
""" testing the tracking number generation route """

from business.models import Business_owner
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from user.models import User

class TestTrackingEndpoint(APITestCase):
    """ Test class for the tracking generation Endpoint """
    
    def setUp(self):
        
        self.user = User.objects.create(
                name='Jane Doe',
                email='Jane.Doe@tester.com',
                phone_number='09015885211',
                address='Lagos',
                password='password',
                account_type='business'
                )
        self.token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"%self.token)
        self.business = Business_owner.objects.create(user=self.user, business_name='Hue Logistics')

    def test_tracking_generation(self):
        print(self.user)
