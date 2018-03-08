from django.conf.urls import url

import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^(?P<user_id>\d+)/$', views.account, name='account'),
    url(r'^(?P<user_id>\d+)/change_name/$', views.change_name, name='change_name'),
    url(r'^(?P<user_id>\d+)/change_email/$', views.change_email, name='change_email'),
    url(r'^(?P<user_id>\d+)/change_password/$', views.change_password, name='change_password'),
    url(r'^(?P<user_id>\d+)/t/(?P<order_id>\d+)/$', views.change_training, name='change_training'),
    url(r'^(?P<user_id>\d+)/c/(?P<order_id>\d+)/$', views.change_consultancy, name='change_consultancy'),
]
