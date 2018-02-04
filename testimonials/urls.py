from django.conf.urls import url

import views

urlpatterns = [
    url('^$', views.show_testimonials, name='testimonials'),
    url(r'^new_testimonial/$', views.new_testimonial, name='new_testimonial'),
]
