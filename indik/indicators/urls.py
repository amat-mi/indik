from django.conf.urls import patterns, include, url
from .views import IndicatorsDataView, IndicatorsList, IndicatorMeta

urlpatterns = patterns('',
    # Examples:
    
    url(r'indicators/(?P<indicator>\w+)/data/$', IndicatorsDataView.as_view(), name='indicators_data'),
    url(r'indicators/(?P<indicator>\w+)/$', IndicatorMeta.as_view(), name='indicator_meta'),
    url(r'indicators/$', IndicatorsList.as_view(), name='indicators_list'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
