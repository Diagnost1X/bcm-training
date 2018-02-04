from django.conf.urls import url

import views

urlpatterns = [
    url('^$', views.show_testimonials, name='testimonials'),
    url(r'^new_testimonial/$', views.new_testimonial, name='new_testimonial'),
    url(r'^edit/(?P<testimonial_id>\d+)/$', views.edit_testimonial, name='edit_testimonial'),
    url(r'^delete/(?P<testimonial_id>\d+)/$', views.delete_testimonial, name='delete_testimonial'),
]
