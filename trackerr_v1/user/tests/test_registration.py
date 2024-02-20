from django.test import TestCase
from user.models import User
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
        
        data = User.objects.get(id=user.id)
        
        self.assertEqual(data.name, 'Jane Doe')     
