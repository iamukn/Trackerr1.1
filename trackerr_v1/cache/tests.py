from django.test import TestCase, Client
from .models import Phone

# Create your tests here.

class TestPhone(TestCase, Client):

    def setUp(self):
        Phone.objects.create(model='ukaegbuu', imei=12345)
        Phone.objects.create(imei=12345, model='ndukwee')
        self.data = Phone.objects.all()


    def test_phones_model(self):

        ukaegbu = self.data.get(model='ukaegbuu')

        self.assertEqual(ukaegbu.model, 'ukaegbuu')
        self.assertEqual(ukaegbu.imei, 12345)


    def test_phones_imei(self):
        ndukwe = self.data.get(model='ndukwee')
        self.assertEqual(ndukwe.model, 'ndukwee')
        self.assertEqual(ndukwe.imei, 12345)

    def test_delete_model(self):
        data = self.data.get(model='ndukwee')

        data.delete()
        with self.assertRaises(Phone.DoesNotExist):
            data = self.data.get(model='ndukwee')

    def test_response(self):

        res = self.client.get('/cache/')
        data = res.content.decode('utf-8')
        self.assertEqual(data,'[{"id":7,"model":"ukaegbuu","imei":12345},{"id":8,"model":"ndukwee","imei":12345}]')
        
        self.assertEqual(res.status_code, 200)
