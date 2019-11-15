from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^add/maps/distance.html', views.distance_calculator, name='distance_calculator'),
    #url(r'^add/maps/$', views.form_view, name='add_map'),
    url(r'^add/maps/$', views.add_map, name='add_map'),
    url(r'^maps/(?P<id>\d+)/$', views.distance_output, name='distance_output'),
]