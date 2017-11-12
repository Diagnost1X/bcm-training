from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.our_services, name='our_services'),
]
