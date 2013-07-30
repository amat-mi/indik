
import itertools
import json
import re

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, FormMixin
from django.views.generic.list import ListView, BaseListView
from django.views.generic.base import TemplateResponseMixin
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy,reverse
from django.core.serializers.json import DjangoJSONEncoder



from django.db.models import Avg, Sum, Max, Min, Count
from django.conf.urls import patterns, include, url




class ResponderMixin(object):

    format = "json"
    streaming = False


    def respond(cls, result, format=None, status_code=200):
        format = format or cls.format
        
        if format == "json":
            if cls.streaming:
                streamer =  cls.respond_json_streaming(result)
            else:
                streamer =  cls.respond_json(result)
            mimetype="application/json"

        elif format == "csv":
            if cls.streaming:
                streamer = cls.respond_csv_streaming(result)
            else:
                streamer = cls.respond_csv(result)
            
            mimetype="text/csv"
        else:
            raise ValueError("Unsupported serialization format: %s" % format)
        
        if 'error' in result:
            status_code = 500
        
        return HttpResponse(streamer, status=status_code, mimetype=mimetype)
    

    def respond_json(cls, result):
        return json.dumps(result, cls=DjangoJSONEncoder) 
    

    def respond_json_streaming(cls, result):
        
        if 'error' in result:
            yield json.dumps(result)
        else:
            yield("{")
            yield('"header" : %s' % json.dumps(result['header'], cls=DjangoJSONEncoder) )
            yield('"data" : [')
            for d in result['data']:
                yield '%s' %  json.dumps(d, cls=DjangoJSONEncoder) 
            yield("]")    
            yield("}")
        
        
    def respond_csv(cls, result):
        body = ""
        if 'data' in result:
            if result['data']:
                keys = result['data'][0].keys()
                keys_csv = ";".join(keys)
                body += keys_csv + "\n"
                 
                for x in result['data']:
                    line = [str(x[k]) for k in keys]
                    csv_line = ";".join(line)
                    body += csv_line
                    body += "\n"

        return body
    

    def respond_csv_streaming(cls, result):
        if 'error' in result:
            yield "Error: %s" % result['error']
        else:
            if 'data' in result:
                if result['data']:
                    first_record = result['data'].next()
                    keys, values = first_record.items()
                    keys_csv = ";".join(keys)
                    values_csv = ";".join(values)
                    yield keys_csv + "\n"
                    yield values_csv + "\n"
                     
                for x in result['data']:
                    line = [str(x[k]) for k in keys]
                    csv_line = ";".join(line)
                    yield csv_line + "\n"


