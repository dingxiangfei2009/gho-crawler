from django.conf.urls import url, include

from . import views

app_name = 'visualiser'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^latest/', views.latest, name='latest'),
    url(r'^query/', include('visualiser.queryurls'))
]