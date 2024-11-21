from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import (APITestCase,APIClient,APIRequestFactory, force_authenticate)
from user.models import User
from unittest.mock import patch
from rest_framework.utils.serializer_helpers import (ReturnList, ReturnDict)
from rest_framework_simplejwt.tokens import AccessToken

""" Class Testing the users endpoint"""

class UserTests(APITestCase):

    @patch('business.signals.send_reg_email')
    def setUp(self, mock_reg_email):
        mock_reg_email.return_value.apply_async = None
        self.user = User.objects.create(
            name='Rena',
            email='rere@gmail.com',
            phone_number='090',
            password='password',
            address='hello',
            account_type='business',
                )
        self.token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"%self.token)
        self.data = {'name':'Rena','email':'johndoe@gmail.com','password':'password', 'phone_number':'099', 'address':'hello','account_type': 'business', 'business_name': 'Meta', "service": 'parcel delivery'}

    @patch('business.signals.send_reg_email')
    def test_create_a_business_user(self, mock_reg_email):
        mock_reg_email.return_value.apply_async = None
        """ 
        Test  to create a business owner
        """

        url = reverse('business-owners-signup')
        res = self.client.post(url, data=self.data, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(type(res.data), ReturnDict)
        self.assertEqual(res.data.get('user').get('name'), 'rena')

    def test_retrieve_users_data(self):
        """
        Ensure we can get all users data
        """
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        url = reverse('users')
        res = self.client.get(url, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(type(res.data), ReturnList)

    def test_retrieve_a_user_data(self):
        """
        Ensure we can get a user data
        """
        # Make the test user an admin user
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        url = reverse('user', kwargs={'pk':self.user.pk})
        req = self.client.get(url)
                
        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(req.data.get('name'), 'Rena')
        self.assertEqual(type(req.data), ReturnDict)        

    def test_to_delete_user(self: None) -> None:

        url = reverse('user', kwargs={'pk':self.user.id})
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT) 
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_users_count_get(self: None) -> None:
        
        # Make the test user an admin user
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        # Query the count url
        url = reverse('users-count')

        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(type(res.data), int)
