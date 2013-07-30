from django.conf.urls import patterns, include, url
from .views import IndicatorsView

urlpatterns = patterns('',
    # Examples:
    url(r'(?P<indicator>\w+)/$', IndicatorsView.as_view(), name='indicators'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
