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
        self.data = {'name':'Rena','email':'rerse@gmail.com','password':'password', 'phone_number':'099', 'address':'hello','account_type': 'business', 'business_name': 'Meta'}

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
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get('name'), 'Rena')
        self.assertEqual(type(res.data), ReturnDict)        

    def test_to_delete_user(self: None) -> None:

        url = reverse('user', kwargs={'pk':self.user.id})
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT) 
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
