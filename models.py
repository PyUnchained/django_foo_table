from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from testing.models import TestModelObj


class Table(models.Model):

	name = models.CharField(max_length = 120)
	source_object = models.OneToOneField(ContentType)

	def __str__(self):
		return self.name
