from django.conf.urls import url

import views

urlpatterns = [
    url('^$', views.show_testimonials, name='testimonials'),
]
