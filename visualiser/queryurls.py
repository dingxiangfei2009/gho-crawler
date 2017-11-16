from django.conf.urls import url

from . import query

urlpatterns = [
    url(r'^$', query.default),
    url(r'^country/(?P<country>.+)', query.by_country),
    url(r'^filter$', query.filter_by)
]