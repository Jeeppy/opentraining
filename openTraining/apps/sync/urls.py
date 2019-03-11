from django.conf.urls import url

from openTraining.apps.sync import views


urlpatterns = [
    url(r'^$', views.dashboard, name='activity_list'),
    url(r'^activities/(?P<year>\d+)/(?P<month>\d+)/$', views.activity_list, name='activity_list'),
    url(r'^mensuel/$', views.mensuel, name='mensuel'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^mensuel/(?P<year>\d+)/$', views.mensuel, name='mensuel'),
    url(r'^synchroniser/$', views.synchroniser, name='synchroniser'),
    url(r'^charges/$', views.charges, name='charges'),
    url(r'^charges/(?P<year>\d+)/(?P<week>\d+)/$', views.charges, name='charges'),
]
