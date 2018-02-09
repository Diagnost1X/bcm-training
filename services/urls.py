from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.our_services, name='our_services'),
    url(r'^consultancy/(?P<consultancy_id>\d+)/$', views.consultancy, name='consultancy'),
    url(r'^training/(?P<training_id>\d+)/$', views.training, name='training'),
]
