import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numbers
import os
from datetime import date, datetime
from django.db import models
from django.db.models.fields.reverse_related import ManyToOneRel
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings

BAD_FIELDS = [models.ForeignKey, models.ManyToManyField, ManyToOneRel, GenericRelation]

def generate_tables(*model_classes):
    tables = {}
    for mc in model_classes:
        tables[mc] = ModelTableManager(mc)


def custom_agg(x):
    print 'Custom Agg'
    print type(x)
    return len(x)

class ModelTableManager():

    def __init__(self, model):
        self.model_class = model
        self.attr_relations = self.get_attr_relations()
        self.columns = []
        self.values = []
        self.indexes = [v['verbose_name'] for k, v in self.attr_relations.iteritems()]
        self.table = self.build()
        self.agg_funcs_available = {'sum':np.sum, 'mean':np.mean, 'min':np.min,
            'max': np.max}

    def get_form_choices(self):
        """
        Returns the available columns, values and indexes in the same format as a Django form
        would normally expect for a form field.
        """
        choices = {'indexes':[], 'columns':[], 'values':[]}
        for i in self.indexes:
            choices['indexes'].append((i.replace('_',' ').title(),
                i.replace('_',' ').title()))
        for i in self.columns:
            choices['columns'].append((i.replace('_',' ').title(),
                i.replace('_',' ').title()))
        for i in self.values:
            choices['values'].append((i.replace('_',' ').title(),
                i.replace('_',' ').title()))
        return choices



    def get_attr_relations(self):
        ignored_fields = ['id']
        relations = {}
        property_list = self.get_properties()
        for p in property_list:
            relations[p] = {'verbose_name':p.replace('_', ' ').title()}
        for f in self.model_class._meta.get_fields():
            if f.name not in ignored_fields and type(f) not in BAD_FIELDS:
                relations[f.name] = {'verbose_name':f.verbose_name.replace('_', ' ').title()}

        return relations

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
        self.indexes = ['ID'] + self.indexes #Register this ID as an available index
        for c in self.attr_relations.keys():
            table[c] = []
            

        for obj in query_set:
            table['ID'].append(str(obj))
            for attr_name in self.attr_relations.keys():
                val = getattr(obj, attr_name)

                if attr_name == 'pregnant':
                    print 'Found P'

                #If this is a number, make sure the attribute is listed as one of
                #the possible values, but not listed as a possible column.
                if isinstance(val, numbers.Number):
                    if attr_name.replace('_', ' ').title() not in self.values:
                        self.values.append(attr_name.replace('_', ' ').title())
                else:
                    if attr_name.replace('_', ' ').title() not in self.columns:
                        self.columns.append(attr_name.replace('_', ' ').title())

                #Handle foreign_key fields
                if inspect.isclass(val):
                    val = str(val)

                if isinstance(val, date) or isinstance(val, datetime):
                    val = str(val)

                table[attr_name].append(val)

        #Rename the keys in the dictionary to the verbose name
        for c in self.attr_relations.keys():
            if c.replace('_', ' ').title() in self.values:
                for index, entry in enumerate(table[c]):
                    if entry == None:
                        table[c][index] = 0
            val = table.pop(c)
            table[self.attr_relations[c]['verbose_name']] = val

        #Remove any of the numerical values from the list of available indexes
        for v in self.values:
            if v in self.indexes:
                self.indexes.remove(v)


        return pd.DataFrame(table)

    def pivot_table(self,form_data, return_path = False):

        
        index = form_data['indexes']
        values = form_data['values']
        columns = form_data['columns']

        #Select the aggregation value to use for each value
        agg_funcs = {}
        for func in self.agg_funcs_available:
            selected_values = form_data[func]
            for v in selected_values:
                agg_funcs[v] = self.agg_funcs_available[func]
        #If none are explicitly set, default to providing the sum of each value
        if agg_funcs == {}:
            agg_funcs = np.sum
        
        if index == []:
            index = self.indexes[0]
        if values == []:
            values = self.values



        ans = pd.pivot_table(self.table,
            index = index, columns = columns,
            fill_value=0, values = values, aggfunc = agg_funcs)

        folder_name = 'latest_pivot_table'
        output_folder = os.path.join(settings.MEDIA_ROOT,
            folder_name)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        file_name = 'pivot_table.xlsx'
        output_file_path = os.path.join(output_folder,
            file_name)
        ans.to_excel(output_file_path,'Response')
        print ans
        
        if return_path:
            return os.path.join(settings.MEDIA_URL,
            '{0}/{1}'.format(folder_name, file_name))
        return ans


