from django.test import TestCase
from business.models import Business_owner
from user.models import User


""" 
  OneToOne Relationship of the User Model with the Business_owner Model
"""

class Business_owner_registration_test(TestCase):

    def test_can_inherit_business_owner_model(self):
        user = User.objects.create(name="Jane Doe", email='janedoe@gmail.com', phone_number='+2347037******', address='Lagos', account_type='Business', password='hello world')
        user.save()
        business_owner = Business_owner.objects.create(user=user, service='Parcel Delivery', business_name='Ukn logistics')
        business_owner.save()

        self.assertEqual(type(business_owner.user.name), str)
