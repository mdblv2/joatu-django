from django.conf.urls.defaults import *

from apps.search.views import search

urlpatterns = patterns('',
    url(r'^$', 'apps.search.views.search', name='search_results'),
)
