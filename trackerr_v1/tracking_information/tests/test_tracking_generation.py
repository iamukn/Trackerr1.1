#!/usr/bin/python3
""" testing the tracking number generation route """

from business.models import Business_owner
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, MagicMock
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from user.models import User

class TestTrackingGenerationEndpoint(APITestCase):
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
        self.data = {'product': 'Medicine','shipping_address':'Authority avenue ikotun lagos','customer_email':'JohnDoe@gmail.com', 'country': 'Nigeria', 'quantity': 2, 'delivery_date': '2024-12-12'}
        self.token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"%self.token)
        self.business = Business_owner.objects.create(user=self.user, business_name='Hue Logistics')
        self.return_value = {'address': 'Authority Ave, Alimosho, Nigeria', 'customer_email':self.data['customer_email'],'city': 'Lagos', 'country': 'Nigeria', 'latitude': 6.54219, 'longitude': 3.22122}
        self.track_num = 'J123456778OE'

    @patch('tracking_information.utils.tracking_class.Track_gen')
    @patch('tracking_information.utils.validate_shipping_address.verify_address')
    def test_tracking_generation_by_business_owner(self, mock_track_gen, mock_verify_address):
        # test to ensure that business users only creates tracking
        url = reverse('generate-tracking')
        mock_track_gen_instance = MagicMock()
        mock_verify_address_instance = MagicMock()

        mock_track_gen_instance.generate_tracking_number.return_value = self.track_num
        mock_track_gen.return_value = mock_track_gen_instance

        mock_verify_address.return_value = self.return_value

        res = self.client.post(url, data=self.data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(type(res.data), ReturnDict)

    @patch('tracking_information.utils.validate_shipping_address.verify_address')
    @patch('tracking_information.utils.tracking_class.Track_gen')
    def test_raises_a_404_for_missing_required_fields(self, mock_track_gen, mock_verify_address):
        # test to ensure that a 404 is raised if required fields aren't provided
        mock_track_gen_instance = MagicMock()
        mock_verify_address_instance = MagicMock()
        mock_track_gen_instance.generate_tracking_number.return_value = self.track_num
        mock_track_gen.return_value = mock_track_gen_instance
        data = self.data
        data.pop('quantity')
        mock_verify_address.return_value = self.return_value
        url = reverse('generate-tracking')
        res = self.client.post(url, data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('tracking_information.utils.validate_shipping_address.verify_address')
    @patch('tracking_information.utils.tracking_class.Track_gen')
    def test_raises_a_401_when_generating_tracking_by_a_non_business_owner(self, mock_track_gen, mock_verify_address):
        # method raises a 401 if a non business owner hits the generate tracking number endpoint
        #mocks the Track_gen and verify_address methods that yield dynamic data
        mock_track_gen_instance = MagicMock()
        mock_verify_address_instance = MagicMock()
        mock_track_gen_instance.generate_tracking_number.return_value = self.track_num
        mock_track_gen.return_value = mock_track_gen_instance
        mock_verify_address.return_value = self.return_value
        # makes the api query
        url = reverse('generate-tracking')
        # modifies the account_type to logistics
        self.user.account_type = 'logistics'
        self.user.save()
        res = self.client.post(url, data=self.data, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    @patch('tracking_information.utils.validate_shipping_address.verify_address')
    @patch('tracking_information.utils.tracking_class.Track_gen')
    def test_return_tracking_history_for_a_unique_email(self, mock_track_gen, mock_verify_address):
        mock_track_gen_instance = MagicMock()
        mock_verify_address_instance = MagicMock()
        mock_track_gen_instance.generate_tracking_number.return_value = self.track_num
        mock_track_gen.return_value = mock_track_gen_instance
        mock_verify_address.return_value = self.return_value

        url = reverse('generate-tracking')
        res = self.client.post(url, data=self.data, format='json')
        url2 = reverse('history')
        res2 = self.client.get(url2, data={'email':self.data['customer_email']})
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
