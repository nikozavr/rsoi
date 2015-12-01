from django.conf.urls import include, url

from manufacturers import views

urlpatterns = [
	url(r'^list/$', views.list, name='list'),	
	url(r'^list/(?P<manufacturer_id>[0-9]+)/$', views.list_num, name='list_num'),	
	url(r'^remove/$', views.remove, name='remove'),	
	url(r'^add/$', views.add, name='add'),	
]