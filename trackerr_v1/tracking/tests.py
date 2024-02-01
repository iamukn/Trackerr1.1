from django.test import TestCase
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient
from .models import Tracking
from django.urls import reverse, reverse_lazy

class Tester(APITestCase):

    def setUp(self):
        self.data = Tracking.objects.all()
        for i in range(12):
            self.data.create(tracking_num=[f'Tester {i}'])
        return super().setUp()    
        
    def TearDown(self):
        return super().tearDown()

class Testers(Tester):

    def test_get(self):
        url = '/tracking/1/'
        data = self.client.get(url) 
        self.assertEqual(data.status_code, 200)


