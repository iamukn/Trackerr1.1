from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import (APITestCase,APIClient,APIRequestFactory, force_authenticate)
from user.models import User
from rest_framework.utils.serializer_helpers import (ReturnList, ReturnDict)
from rest_framework_simplejwt.tokens import AccessToken

""" Class Testing the users endpoint"""

class UserTests(APITestCase):

    def setUp(self):
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
        self.data = {'id': 1, 'name':'Rena','email':'rerse@gmail.com','password':'password', 'phone_number':'099', 'address':'hello','account_type': 'business', 'business_name': 'Meta'}

    def test_create_a_business_user(self):
        """ 
        Test  to create a business owner
        """

        url = reverse('business-owners')
        res = self.client.post(url, data=self.data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(type(res.data), ReturnDict)
        self.assertEqual(res.data.get('user').get('name'), 'Rena')

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
