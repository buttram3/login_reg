from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add_appointment$', views.add_appointment),
    url(r'^appointments$', views.appointments),
    url(r'^delete_appointment/(?P<task_id>\d+)$', views.delete_appointment),
    url(r'^edit_appointment/(?P<task_id>\d+)$', views.edit_appointment),
]
