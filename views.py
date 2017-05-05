import traceback

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType  

from templatetags.forms import TableFooHelperForm
from templatetags.helpers import ModelTableManager

# Create your views here.
def export_to_excel(request, source_ct_pk):

    if not request.POST:
        print 'Way 1'
        return None

    try:
        source_ct_instance = ContentType.objects.get(pk = source_ct_pk)
        source_ct = source_ct_instance.model_class()
        tm = ModelTableManager(source_ct)
        form = TableFooHelperForm(request.POST, **tm.get_form_choices())
        if form.is_valid():
            output_file = tm.pivot_table(form.cleaned_data,
                return_path = True)
            resp_msg = """Success. Click <a href = '{0}'
                target = '_blank'>here</a> to download.""".format(output_file)
            return JsonResponse({'success':True,
                'msg':resp_msg})

        else:
            form_html = render_to_string('change_form_helper.html',
                {'form':form, 'source_ct':source_ct_instance}, request)
            return JsonResponse({'form_with_errors':form_html, 'success':False,
                'reset_button':True})

    #Some internal server error occured
    except Exception as e:
        print 'Exception'
        return JsonResponse(
            {'msg': traceback.format_exc(), 'success':False})

