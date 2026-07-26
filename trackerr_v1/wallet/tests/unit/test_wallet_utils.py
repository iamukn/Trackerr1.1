from django.test import SimpleTestCase
from wallet.utils.calc_vat import calc_vat
from decimal import Decimal

class TestUnits(SimpleTestCase):

    def test_calc_vat(self):
        gh_vat = calc_vat(10, 'ghana')
        ng_vat = calc_vat(1000, 'nigeria')
        # assertions
        self.assertEqual(gh_vat, Decimal('0.2000000000000000111022302463'))
        self.assertEqual(ng_vat, Decimal('15.00'))
