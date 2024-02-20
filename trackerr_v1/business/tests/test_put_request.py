from django.urls import reverse
from rest_framework import status
from user.models import User
from business.models import Business_owner
from business.serializers import Business_ownerSerializer
from user.serializers import UsersSerializer
from rest_framework.test import APITestCase

""" testing the HTTP methods [PUT, PATCH, DELETE] requests on the business app """

class BusinessTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create(
            name='Rena',
            email='rere@gmail.com',
            phone_number='090',
            address='hello',
            password='password',
            account_type='business'
                )

        self.business = Business_owner.objects.create(user=self.user, business_name='haplotype')



    def test_put(self):
        data = {'user':{'name':'Richard','email':'rere@gmail.com', 'password':'password11', 'phone_number':'0901588', 'address':'Abuja','account_type': 'business'}, 'business_name':'dabidab'}
        
        url = reverse('business-owner-route', kwargs={'id':self.business.id})
        res = self.client.put(url, data=data, format='json')
        
        self.assertEqual(res.data['user'].get('name'), 'Richard')
        self.assertEqual(res.status_code, status.HTTP_206_PARTIAL_CONTENT)
