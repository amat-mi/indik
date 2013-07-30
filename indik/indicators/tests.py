"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from indicators.import_helpers import IndicatorManager

class SimpleTest(TestCase):

    def test_loader(self):
        w = IndicatorManager()
        w.drop_indicator("L4")
        w.import_file("samples/L4_Velocit%E0_commerciale_TPL.xlsx")

    def test_drop(self):
        pass
        #w = IndicatorManager()
        #w.drop_indicator("L4")