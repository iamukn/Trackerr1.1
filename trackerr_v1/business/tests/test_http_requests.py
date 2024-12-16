from django.urls import reverse
from rest_framework import status
from user.models import User
from business.models import Business_owner
from business.serializers import Business_ownerSerializer
from user.serializers import UsersSerializer
from unittest.mock import patch, MagicMock
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

""" testing the HTTP methods [PUT, PATCH, DELETE] requests on the business app """

class BusinessTest(APITestCase):
    
    @patch('business.signals.send_reg_email')
    def setUp(self, mock_reg_email):
        mock_reg_email.return_value.apply_async = None
        self.user = User.objects.create(
            name='Rena',
            email='rere@gmail.com',
            phone_number='090',
            address='hello',
            password='password',
            account_type='business'
                )
        self.token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"%self.token)
        self.business = Business_owner.objects.create(user=self.user, business_name='haplotype')
        self.data = {'name':'richard','email':'rere@gmail.com', 'password':'password11', 'phone_number':'0901588', 'address':'Abuja','account_type': 'business', 'business_name':'dabidab'}
        self.return_value = {'address': '36b authority avenue', 'city': 'Lagos', 'country': 'Nigeria', 'latitude': 6.54219, 'longitude': 3.22122} 

    @patch('business.signals.send_reg_email.apply_async')
    @patch('business.views.views.verify_shipping_address.apply_async')
    def test_create_a_business_onwer(self, mock_apply, mock_email):
        mock_instance = MagicMock(return_value=self.return_value)
        mock_apply.return_value.get = mock_instance
        
        url = reverse('business-owners-signup')
        data = self.data
        data['service'] = 'parcel delivery'
        data['email'] = 'janedoe1212@gmail.com'
        res = self.client.post(url, data=data, format='json')
        # mock email
        mock_email_instance = MagicMock(return_value="Registration email sent")
        mock_email.return_value = mock_email_instance
        mock_email.assert_called_once()
        mock_apply.assert_called_once()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_put(self):
        data = self.data
       
        url = reverse('business-owner-route', kwargs={'id':self.business.id})
        res = self.client.put(url, data=data, format='json')
        
        self.assertEqual(res.data['user'].get('name'), 'richard')
        self.assertEqual(res.status_code, status.HTTP_206_PARTIAL_CONTENT)

    def test_patch(self):
        data = {'name': 'Lovina Davies',"business_name": "Volta Charger"}
        url = reverse('business-owner-route', kwargs={'id':self.business.id})
        res = self.client.patch(url, data=data, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_206_PARTIAL_CONTENT)
        

    def test_delete(self):
        
        url = reverse('business-owner-route', kwargs={'id':self.business.id})
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, 204)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    """ Total counts of business owners routes """

    def test_business_owners_count(self):
        url = reverse('business-counts')
        # Makes the test user an admin
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        # Make a request to the count endpoint
        res = self.client.get(url, format='json')
        # carry out test assertions
        self.assertTrue(type(res.data), int)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_can_fetch_tracking_number_counts(self):
        # checks to see if the status count endpoint works
        url = reverse('status-count')
            
        res = self.client.get(url)
        # asserts if the returned data contained the returned_status_count field
        self.assertTrue( "returned_status_count",  "total_tracking_generated" in res.data)
        # asserts if the returned data is a dictionary
        self.assertTrue(type(res.data) is dict)
        # asserts if the response code is 200_OK
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_can_fetch_weekly_activity_chart(self):
        # checks to see if the weekly data is retrieved successfully
        url = reverse('weekly-activity')
        # make a request to the endpoint
        response = self.client.get(url, format='json')
        self.assertTrue('Mon' and 'Tue' and 'Wed' and 'Thur' and 'Fri' in response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue( isinstance(response.data, dict))

    def test_can_fetch_monthly_activity_chart(self):
        # checks to see if the monthly data is retrieved successfully
        url = reverse('monthly-activity')
        # make a request to the endpoint
        response = self.client.get(url, format='json')
        self.assertTrue('Week One' and 'Week Two' and 'Week Three' and 'Week Four' in response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue( isinstance(response.data, dict))
