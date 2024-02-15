from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User
from rest_framework.utils.serializer_helpers import (ReturnList, ReturnDict)

""" Class Testing the users endpoint"""

class UserTests(APITestCase):
    def test_retrieve_users_data(self):
        """
        Ensure we can get all users data
        """

        url = reverse('users')
        res = self.client.get(url, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(type(res.data), ReturnList)

