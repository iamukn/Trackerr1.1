from django.test import TestCase
from user.models import User, Logistics_partner, Business_owner
from django.core.exceptions import ValidationError


class RegistrationTest(TestCase):
    """ Tests """
    def test_cant_register_with_partial_data(self):
        # test to see if the registration functionality for the user model works 
        # with partial data or will raise a ValidationError
        with self.assertRaises(ValidationError):
            user = User.objects.create(name="John Doe", email='johndoe@gmail.com', phone_number='07037678783', address='Lagos', account_type='Business')
            if not user.full_clean():
                raise ValidationError

    def test_can_register(self):
        # test to see if the registration functionality for the user model works
        user = User.objects.create(name="Jane Doe", email='janedoe@gmail.com', phone_number='+2347037******', address='Lagos', account_type='Business', password='helloworld')
        if user.full_clean():
            user.save()

        self.assertEqual(type(user.name), str)

    def test_can_inherit_logistic_partner_model(self):
        #test to see if the User Model can be inherited by the Logistics Model
        user = User.objects.create(name="Jane Doe", email='janedoe@gmail.com', phone_number='+2347037******', address='Lagos', account_type='Business', password='Hello')
        user.save()
        logistics_partner = Logistics_partner.objects.create(user=user)
        logistics_partner.save()

        self.assertEqual(type(logistics_partner.user.name), str)

    def test_can_inherit_business_owner_model(self):

        user = User.objects.create(name="Jane Doe", email='janedoe@gmail.com', phone_number='+2347037******', address='Lagos', account_type='Business', password='heillo')
        user.save()
        business_owner = Business_owner.objects.create(user=user, service='Parcel Delivery', business_name='Ukn logistics')
        business_owner.save()

        self.assertEqual(type(business_owner.user.name), str)
