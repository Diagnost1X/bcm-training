from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.contact_us, name='contact_us'),
]
