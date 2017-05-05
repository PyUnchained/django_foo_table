from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy  
from django import forms 
from django.utils.html import escape

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Submit, Field
from crispy_forms.bootstrap import InlineCheckboxes





class TableFooHelperForm(forms.Form):

    source_ct = forms.ModelChoiceField(queryset = ContentType.objects.all())
    values = forms.MultipleChoiceField(choices = [], required = False)
    indexes = forms.MultipleChoiceField(choices = [], required = False)
    columns = forms.MultipleChoiceField(choices = [], required = False)

    sum = forms.MultipleChoiceField(choices = [], required = False)
    mean = forms.MultipleChoiceField(choices = [], required = False)
    min = forms.MultipleChoiceField(choices = [], required = False)
    max = forms.MultipleChoiceField(choices = [], required = False)

    def __init__(self, *args, **kwargs):
        self.aggregate_fields = ['sum', 'mean', 'min', 'max']
        index_choices = kwargs.pop('indexes')
        column_choices = kwargs.pop('columns')
        value_choices = kwargs.pop('values')
        super(TableFooHelperForm, self).__init__(*args, **kwargs)

        self.fields['values'].choices = value_choices
        for field in self.aggregate_fields:
            self.fields[field].choices = value_choices
        self.fields['indexes'].choices = index_choices
        self.fields['columns'].choices = column_choices
        self.fields['source_ct'].widget = forms.HiddenInput()

        self.helper = FormHelper()
        self.helper.form_id = 'table_foo_helper_form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset('Structure',
                'source_ct',
                Field('values', css_class = 'inline-input'),
                Field('indexes', css_class = 'inline-input'),
                Field('columns', css_class = 'inline-input'),
            ),
            Fieldset('Aggregation',
                'sum',
                'mean',
                'min',
                'max',
            ),
            
            ButtonHolder(
                Submit('submit', 'Generate Pivot Table',
                    css_class='button white',
                    css_id="table_foo_helper_form_submit")
            )
        )

    def clean(self):
        cleaned_data = super(TableFooHelperForm, self).clean()
        duplicated_values = []
        for field in self.aggregate_fields:
            for other_field in self.aggregate_fields:
                #Dont compare the fields if they are the same
                if field == other_field:
                    continue

                for entry in cleaned_data.get(field):
                    if entry in cleaned_data.get(other_field) and entry not in duplicated_values:
                        duplicated_values.append(entry)

        if len(duplicated_values) > 0:
            msg = """The following values have been designated to more than one
            aggregate function: {0}.""".format(','.join(duplicated_values))
            raise forms.ValidationError(escape(msg))

