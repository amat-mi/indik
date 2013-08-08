#from .views_mixins import *
from django.views.generic import View
from django.views.generic.list import BaseListView
from .models import *
from django.http import HttpResponse



class BaseRespondMixin(object):
    def respond(cls, result, format=None, status_code=200):
        
        mimetype="application/json"
        out = ''
        
        if 'error' in result:
            status_code = 500

        if 'data' in result:
            out  = "[" +    ",".join([d.to_json() for d in result['data']]) + "]"

        return HttpResponse(out, status=status_code, mimetype=mimetype)



class IndicatorsList(BaseRespondMixin, BaseListView):
    
    def get(self, request, *args, **kwargs):
        """
        """
        format = request.GET.get('format', None)
        try:
            result = self.get_wrapped(request, *args, **kwargs)
            return self.respond(result, status_code=200, format=format)
        except Exception, e:
            result = {'error' : str(e) }
            import traceback            
            traceback.print_exc()
            return self.respond(result, status_code=500, format=format)   

    def get_wrapped(self, request, *args, **kwargs):
        """
        """
        objects = IndicatorDescriptor.objects
        return { 'data' : objects }


class IndicatorsView(BaseRespondMixin, BaseListView):
    
    
    def respond(cls, result, format=None, status_code=200):
        
        mimetype="application/json"
        out = ''
        
        if 'error' in result:
            status_code = 500

        if 'data' in result:
            out  = "[" +    ",".join([d.to_json() for d in result['data']]) + "]"

        return HttpResponse(out, status=status_code, mimetype=mimetype)


    

        

    def get(self, request, *args, **kwargs):
        """
        """
        format = request.GET.get('format', None)
        try:
            result = self.get_wrapped(request, *args, **kwargs)
            return self.respond(result, status_code=200, format=format)
        except Exception, e:
            result = {'error' : str(e) }
            import traceback            
            traceback.print_exc()
            return self.respond(result, status_code=500, format=format)   


    def get_filters(self, filters):
        out = {}
        for f in filters:
            pieces = f.split(":")
            out[pieces[0]] = int(pieces[1])
        return out


    def get_wrapped(self, request, *args, **kwargs):
        """
        """
        indicator_code = kwargs.get('indicator')

        filters = request.GET.getlist('filter')
        orders = request.GET.getlist('order')
        fields = request.GET.getlist('field')
        
        fi = self.get_filters(filters)
        objects = IndicatorData.objects(code=indicator_code, **fi)[:100]

        


        return { 'data' : objects }

        
        
