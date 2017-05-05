from django import template


from django.contrib.contenttypes.models import ContentType  
from django import forms 

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from helpers import ModelTableManager
from .forms import TableFooHelperForm

register = template.Library()

@register.inclusion_tag('change_form_helper.html')
def table_foo_helper(obj):
    tm = ModelTableManager(obj.source_object.model_class())
    form = TableFooHelperForm(initial = {'source_ct':obj.source_object},
        **tm.get_form_choices())
    return {'form':form, 'source_ct':obj.source_object}