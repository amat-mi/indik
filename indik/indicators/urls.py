from django.conf.urls import patterns, include, url
from .views import IndicatorsView, IndicatorsList

urlpatterns = patterns('',
    # Examples:
    
    url(r'data/(?P<indicator>\w+)/$', IndicatorsView.as_view(), name='indicators'),
    url(r'list/$', IndicatorsList.as_view(), name='indicators_list'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
