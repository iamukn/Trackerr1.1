from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Books

class TestBook(APITestCase):
    

    def test_patch(self):
        data = Books.objects.create(author='Daniel', message='Hello there')
        update_data = { "author": "IkpaMor"}
        req = self.client.patch(f'/drf/myviewset/{data.id}/', update_data, format='json')

        self.assertTrue(req.status_code <= 300)


# Create your tests here.
