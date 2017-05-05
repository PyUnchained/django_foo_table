from django.test import TestCase

from tables import ModelTableManager
from testing.models import TestModelObj

# Create your tests here.
class TableManagerTestCase(TestCase):

	def setUp(self):
		for i in range(0,5):
			TestModelObj.objects.create(
				attr_1 = 'T{0}'.format(i))

	def test_initialization(self):
		tm = ModelTableManager(TestModelObj)
		#Check that columns are correct
		#Check that the table is as expected

		print tm.pivot_table()
