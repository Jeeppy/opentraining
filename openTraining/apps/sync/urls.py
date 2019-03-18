from django.conf.urls import url

from openTraining.apps.sync import views


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^journal/(?P<year>\d+)/(?P<month>\d+)/$', views.journal, name='activity_list'),
    url(r'^journal/$', views.journal, name='journal'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^bilan/$', views.bilan, name='bilan'),
    url(r'^bilan/(?P<year>\d+)/$', views.bilan, name='bilan'),
    url(r'^synchroniser/$', views.synchroniser, name='synchroniser'),
    url(r'^charges/$', views.charges, name='charges'),
    url(r'^charges/(?P<year>\d+)/(?P<week>\d+)/$', views.charges, name='charges'),
]
