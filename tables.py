import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numbers
from django.db import models
from django.db.models.fields.reverse_related import ManyToOneRel

BAD_FIELDS = [models.ForeignKey, models.ManyToManyField, ManyToOneRel]

def generate_tables(*model_classes):
	tables = {}
	for mc in model_classes:
		tables[mc] = ModelTableManager(mc)

class ModelTableManager():

	def __init__(self, model):
		self.model_class = model
		self.columns = self.get_columns()
		self.values = []
		self.index = [v['verbose_name'] for k, v in self.columns.iteritems()]
		self.table = self.build()

	def get_columns(self):
		ignored_fields = ['id']
		columns = {}
		property_list = self.get_properties()
		for p in property_list:
			columns[p] = {'verbose_name':p.replace('_', ' ').title()}
		for f in self.model_class._meta.get_fields():
			if f.name not in ignored_fields and type(f) not in BAD_FIELDS:
				columns[f.name] = {'verbose_name':f.verbose_name}

		return columns

	def get_properties(self):
		base_properties = []
		bases = self.model_class.__bases__
		for b in bases:
			b_props = [name for name, value in vars(b).items() if isinstance(value, property)]
			base_properties += b_props

		cls_properties = [name for name, value in vars(self.model_class).items() if isinstance(value, property)]
		return base_properties + cls_properties




	def build(self, query_set = None):
		import inspect
		if query_set == None:
			query_set = self.model_class.objects.all()

		table = {}
		table['ID'] = []
		self.index = ['ID'] + self.index #Register this ID as an available index
		for c in self.columns.keys():
			table[c] = []
			

		for obj in query_set:
			table['ID'].append(str(obj))
			for attr_name in self.columns.keys():
				val = getattr(obj, attr_name)

				#If this is a number, make sure the attribute is listed as one of
				#the possible values.
				if isinstance(val, numbers.Number) and attr_name not in self.values:
					self.values.append(attr_name)

				#Handle foreign_key fields
				if inspect.isclass(val):
					val = str(val)

				table[attr_name].append(val)

		#Rename the keys in the dictionary to the verbose name
		for c in self.columns.keys():
			val = table.pop(c)
			table[self.columns[c]['verbose_name']] = val





		return pd.DataFrame(table)

	def pivot_table(self, index = [], values = [], columns = []):
		if index == []:
			index = self.index[0]
		if values == []:
			values = self.values

		ans = pd.pivot_table(self.table,
			index = index, columns = columns, fill_value=0,
			aggfunc=np.sum)

		ans.to_excel('/tmp/dem.xlsx','Sheet1')
		return ans


