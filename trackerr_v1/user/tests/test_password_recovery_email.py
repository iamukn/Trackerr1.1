#!/usr/bin/env python3
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from unittest.mock import patch, ANY
from user.models import User
from user.views.password_recovery import Recover_password
from business.models import Business_owner

""" Test the email messaging endpoint for password recovery """


class TestPasswordRecoveryEmailandChange(APITestCase):
    """  password reset test """

    def setUp(self):
        self.user = User.objects.create(
            name = 'Jane Doe',
            email = 'officialtrackerr@gmail.com',
            phone_number='09023456789',
            address='Ikeja, Lagos',
            password='password',
            account_type='business'
                )

        self.token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"%self.token)
        self.business = Business_owner.objects.create(user=self.user, business_name='haplotype')
    
    @patch('user.views.password_recovery.send_recovery_email.delay')
    def test_can_send_recovery_email(self, mock_thread):
        url = reverse('recover-password')
        res = self.client.post(url, data={'email': self.user.email})
        self.assertTrue(res.status_code == 200)
        # mocks the thread in charge of sending recovery emails with a one time token
        mock_thread.assert_called_once_with(email=self.user.email, new_password=ANY)

    def test_change_password(self):
        url = reverse('change-password')
        data = {'password1': 'password', 'password2': 'password'}
        res = self.client.post(url, data=data, format='json')
        self.assertTrue(res.status_code == 206)
