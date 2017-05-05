import random
from django.db import models

class TestModelObj(models.Model):

	attr_1 = models.CharField(max_length = 20, blank = True,
		null = True)

	@property
	def test_property_1(self):
		return random.randrange(0,1000)

	@property
	def test_property_2(self):
		return random.randrange(0,1000)

	@property
	def test_property_3(self):
		return random.randrange(0,1000)
