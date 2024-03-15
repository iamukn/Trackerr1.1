#!/usr/bin/python3
""" testing the tracking number generation route """

from business.models import Business_owner
from django.urls import reverse
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict
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

    def test_tracking_generation_by_business_owner(self):
        # test to ensure that business users only creates tracking
        url = reverse('generate-tracking')
        
        res = self.client.post(url, data={'shipping_address' : 'Lagos, Ibadan exoressway'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(type(res.data), ReturnDict)

    def test_raises_a_404_for_missing_required_fields(self):
        # test to ensure that a 404 is raised if required fields aren't provided
        url = reverse('generate-tracking')
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)