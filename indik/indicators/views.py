import json
from collections import OrderedDict

from django.views.generic import View
from django.views.generic.list import BaseListView
from django.views.generic.base import TemplateView
from django.http import HttpResponse

from .models import *
from .helpers import *



class BaseRespondMixin(object):

    def get(self, request, *args, **kwargs):
        """
        """
        format = request.GET.get('format', None)
        try:
            result = self.get_data(request, *args, **kwargs)
            return self.respond(result, status_code=200, format=format)
        except Exception, e:
            result = {'error' : str(e) }
            import traceback            
            traceback.print_exc()
            return self.respond(result, status_code=500, format=format)   


    @classmethod
    def respond(cls, result, format=None, status_code=200):
        
        mimetype="application/json"
        out = json.dumps(result)
        return HttpResponse(out, status=status_code, mimetype=mimetype)

    @classmethod
    def get_json(self, request, result):
        if 'data' in result:
            result['num_records'] = len(result['data'])

        result['url'] = request.build_absolute_uri()
        return result
        
 


class IndicatorsList(BaseRespondMixin, BaseListView):
    
    def get_data(self, request, *args, **kwargs):
        """
        """
        objects = IndicatorDescriptor.objects
        out_data = list(iterator_serializer(objects))
        return self.get_json(request, { 'data' : out_data })


class IndicatorMeta(BaseRespondMixin, BaseListView):
    
    def get_data(self, request, *args, **kwargs):
        """
        """
        indicator_code = kwargs.get('indicator')
        objects = IndicatorDescriptor.objects(code=indicator_code)
        out_data = list(iterator_serializer(objects))
        return self.get_json(request, { 'data' : out_data })


class IndicatorClasses(BaseRespondMixin, BaseListView):
    
    def get_data(self, request, *args, **kwargs):
        """
        """

        indicator_code = kwargs.get('indicator')
        indicator = IndicatorDescriptor.objects.get(code=indicator_code)
        klasses_dict =  indicator.get_klasses_dict()
        

        #out_data = list(iterator_serializer(objects))
        return self.get_json(request, { 'data' : [ klasses_dict ] })


class IndicatorsDataView(BaseRespondMixin, BaseListView): 

    def get_filters(self, filters, not_convert, klasses):
        out = {}
        for f in filters:
            pieces = f.split(":")
            field_name = pieces[0].split("__")[0] 
            if not_convert and field_name in klasses:
                out[pieces[0]] = pieces[1].replace('"', '')    
            else:
                out[pieces[0]] = float(pieces[1])
        return out


    def get_data(self, request, *args, **kwargs):
        """
        """
        indicator_code = kwargs.get('indicator')
        indicator = IndicatorDescriptor.objects.get(code=indicator_code)
        value_field = indicator.value_field
        klasses_dict =  indicator.get_klasses_dict()
        
        filters = request.GET.getlist('filter')
        aggregation = request.GET.get('aggregation', None) 
        resolve_classes = request.GET.get('resolve_classes', None) 
        resolve_filters = request.GET.get('resolve_filters', None) 
        
        
        fi = self.get_filters(filters, resolve_filters, klasses_dict)
        properties_callbacks = {}

        if resolve_filters:
            #remap filters values to class values
            #this is semplicistic, it assumes that each class value is unique
            for flt in fi:
                field_name = flt.split("__")[0]
                if field_name not in klasses_dict:
                    continue
                intersted_classes =klasses_dict[field_name]
                reverse_classes =  dict (zip(intersted_classes.values(),intersted_classes.keys()))
                fi[flt] = reverse_classes[fi[flt]]
        
        if resolve_classes:
            #prepare properties callbacks   
            for k in klasses_dict:
                def g(x,k):
                    value = x.get(k)
                    try:
                        return klasses_dict[k][value]
                    except Exception, e:
                        return value
                properties_callbacks[k] = g


        if aggregation:
            operator = aggregation
            group_by = request.GET.get('group_by', '')
            if group_by:
                group_fields = group_by.split(":")
            else:
                group_fields = []

            properties_to_remove = [x for x in properties_callbacks if x not in group_fields]
            for p in properties_to_remove:
                del properties_callbacks[p]

            collection = IndicatorData.objects._collection
            objects = group_by_query(collection, operator, value_field, group_fields=group_fields, filter=get_lookup_query(fi))

        else:
            objects = IndicatorData.objects(code=indicator_code, **fi)
            g = lambda x, k:  x.get(value_field)
            properties_callbacks.update({'_value' : g })

        out_data = list(iterator_serializer(objects, properties_callbacks = properties_callbacks))
        

        return self.get_json(request, { 'data' : out_data})

        

class IndicatorsBrowser(TemplateView):
    template_name = "indicators/browser.html"
    

    
