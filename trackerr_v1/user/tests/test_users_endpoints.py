from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User
from rest_framework.utils.serializer_helpers import (ReturnList, ReturnDict)

""" Class Testing the users endpoint"""

class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            name='Rena',
            email='rere@gmail.com',
            phone_number='090',
            address='hello',
            account_type='business'
                )

    def test_retrieve_users_data(self):
        """
        Ensure we can get all users data
        """

        url = reverse('users')
        res = self.client.get(url, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(type(res.data), ReturnList)

    def test_retrieve_a_user_data(self):
        """
        Ensure we can get a user data
        """

        url = reverse('user', kwargs={'pk':self.user.pk})
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(type(res.data), ReturnDict)


    def test_can_edit_a_user_data_using_put(self):
        """
        Ensure we can edit a user data using put
        """
        url = reverse('user', kwargs={'pk':self.user.pk})
        res = self.client.put(url, data={'name':'Duke', 'email':'9ice@gmail.com', 'phone_number':'0707', 'address':'Gidi', 'account_type': 'business'})
        
        self.assertEqual(res.status_code, status.HTTP_206_PARTIAL_CONTENT)
        self.assertEqual(type(res.data), ReturnDict)
