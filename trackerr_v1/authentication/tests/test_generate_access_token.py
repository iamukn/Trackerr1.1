#!/usr/bin/env python3
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from user.models import User
from unittest.mock import patch


""" Login and token generation test """

class TestTokenObtainPair(APITestCase):
    """ 
    This class tests the access token generation
    endpoint for authentication
    """

    def setUp(self):
        self.user = User.objects.create(
           name = 'Doe',
           email = 'iamukn@yahoo.com',
           phone_number = '09015885144',
           address = '1234 county avenue, Washinton DC',
           account_type = 'logistics',
                )
        self.user.set_password('password')
        self.user.save()


    @patch('authentication.views.auth.threading.Thread')
    def test_can_get_login_tokens(self, mock_thread):

        # Configure the mock to do nothing when started
        mock_thread.return_value.start.return_value = None

        url = reverse('token_obtain_pair')
        res = self.client.post(url, data={'email':'iamukn@yahoo.com', 'password': 'password'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in res.data and 'refresh' in res.data)
