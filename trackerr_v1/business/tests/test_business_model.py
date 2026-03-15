from django.test import TestCase
from business.models import Business_owner
from unittest.mock import patch
from user.models import User


""" 
  OneToOne Relationship of the User Model with the Business_owner Model
"""

class Business_owner_registration_test(TestCase):
    # mock the send_email_method
    @patch('business.signals.send_reg_email')
    def test_can_inherit_business_owner_model(self, mock_reg_email):
        mock_reg_email.return_value.apply_async = None
        user = User.objects.create(name="Jane Doe", email='janedoe@gmail.com', phone_number='7037******', address='Lagos', account_type='Business', password='hello world')
        user.save()
        business_owner = Business_owner.objects.create(user=user, service='Parcel Delivery', business_name='Ukn logistics')
        business_owner.save()

        self.assertEqual(type(business_owner.user.name), str)
