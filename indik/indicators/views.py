from .views_mixins import *
from .models import *



class IndicatorsView(ResponderMixin, BaseListView):


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
        indicator_code = kwargs.get('indicator')

        filters = request.GET.getlist('filter')
        orders = request.GET.getlist('order')
        fields = request.GET.getlist('field')
        
        objects = IndicatorData.objects(code=indicator_code)
        return [d.to_json() for d in objects]

        #####
        
        
