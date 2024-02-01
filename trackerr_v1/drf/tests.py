from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Books

class TestBook(APITestCase):
    """Inherited from APITestCase class"""    

    def test_patch(self):
        # created a test object in the database
       
        data = Books.objects.create(author='Daniel', message='Hello there')
        update_data = { "author": "IkpaMor"}
        req = self.client.patch(f'/drf/myviewset/{data.id}/', update_data, format='json')

        self.assertTrue(req.status_code <= 300)


# Create your tests here.
