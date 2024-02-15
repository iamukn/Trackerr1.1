from django.test import TestCase
from user.models import User
from logistics.models import Logistics_partner

""" 
   Tests to check if a User can inherit the Logistics model
"""

class LogisticsRegistrationTest(TestCase):

    def test_can_inherit_logistic_partner_model(self):
        #test to see if the User Model can be inherited by the Logistics Model
        user = User.objects.create(name="Jane Doe", email='janedoe@gmail.com', phone_number='+2347037******', address='Lagos', account_type='Business', password='Hello world')
        user.save()
        logistics_partner = Logistics_partner.objects.create(user=user)
        logistics_partner.save()

        self.assertEqual(type(logistics_partner.user.name), str)
