#!/usr/bin/env python3
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from unittest.mock import patch, ANY, MagicMock
from user.models import User
from user.views.password_recovery import Recover_password
from business.models import Business_owner

""" Test the email messaging endpoint for password recovery """


class TestPasswordRecoveryEmailandChange(APITestCase):
    """  password reset test """

    @patch('business.signals.send_reg_email')
    def setUp(self, mock_reg_email):#, mock_update):
        # mock registration email 
        mock_reg_email.return_value.apply_async= None


        self.user = User.objects.create(
            name = 'Jane Doe',
            email = 'officialtrackerr@gmail.com',
            phone_number='9023456789',
            address='Ikeja, Lagos',
            password='password',
            account_type='business'
                )

        self.token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"%self.token)
        self.business = Business_owner.objects.create(user=self.user, business_name='haplotype')
        self.otp = '123546'

    @patch('user.views.password_recovery.send_recovery_email.delay')
    def test_can_send_recovery_email(self, mock_emailer):
        mock_instance = MagicMock(return_value=None)
        mock_emailer.return_value=mock_instance
        url = reverse('recover-password')
        res = self.client.post(url, data={'email': self.user.email})


        self.assertTrue(res.status_code == 200)
        # mocks the thread in charge of sending recovery emails with a one time token
        mock_emailer.assert_called_once_with(email=self.user.email, new_password=ANY)

    def test_change_password(self):
        url = reverse('change-password')
        data = {'password1': 'password', 'password2': 'password'}
        res = self.client.post(url, data=data, format='json')
        print(res.json())
        self.assertTrue(res.status_code == 206)
 
    @patch('user.views.change_password.send_update_email.delay')
    @patch('user.views.password_recovery.password_gen') 
    def test_update_password(self, mock_otp, mock_reg_email):
        # reset the password
        mock_reg_email_instance = MagicMock(return_value=None)
        mock_reg_email.return_value=mock_reg_email_instance

        url = reverse('recover-password')
        # mock the password_generation function
        mock_otp.return_value=self.otp
        res = self.client.post(url, data={'email': self.user.email})

        # update the password
        url = reverse('update-password')
        data = {'password1': 'password', 'password2': 'password', 'email': self.user.email, 'otp': self.otp}
        res = self.client.post(url, data=data)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        mock_reg_email.assert_called_once_with(email=self.user.email, name=self.user.name)
