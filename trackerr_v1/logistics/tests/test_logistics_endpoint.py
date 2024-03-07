#!/usr/bin/python3
from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from user.models import User
from logistics.models import Logistics_partner


class TestLogisticsEndpoint(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(
            name = 'John Doe',
            email = 'Johndoe@janedoe,com',
            phone_number='+2347037******',
            address='Lagos',
            account_type='Business',
            password='johndoe123'
                )
        self.user.save()

        self.logistics_partner = Logistics_partner.objects.create(user=self.user)
        self.logistics_partner.save()
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"%self.token)


    def test_logistics_partner_count(self):
        url = reverse('logistics-count')
        # Grants the test user a superuser privilege
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(type(res.data), int)
