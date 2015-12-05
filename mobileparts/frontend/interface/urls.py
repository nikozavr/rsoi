from django.conf.urls import include, url

from interface import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name="login"),
	url(r'^logout/', views.logout, name="logout"),
	url(r'^register/', views.register, name="register"),

	url(r'^manufacturers/$',views.manufacturers, name="manufacturers"),
	url(r'^devices/$',views.devices, name="devices"),
	url(r'^parts/$',views.parts, name="parts"),

	url(r'^parts/info/(?P<part_id>[0-9]+)', views.info_part, name="info_part")

#	url(r'^session/', include('session.urls', namespace="session")),
#	url(r'^backend_manufacturers/', include('backend_manufacturers.urls', namespace="backend_manufacturers")),
#	url(r'^backend_devices/', include('backend_devices.urls', namespace="backend_devices")),

#	url(r'^device/add/', views.add_device, name="add_device"),
#	url(r'^manufacturer/add/', views.add_manufacturer, name="add_manufacturer"),
#
#	url(r'^device/(?P<device_id>[0-9]+)/delete/', views.del_device, name="del_device"),
#	url(r'^manufacturer/(?P<manufacturer_id>[0-9]+)/delete/', views.del_manufacturer, name="del_manufacturer"),
#
#	url(r'^device/(?P<device_id>[0-9]+)/edit/', views.edit_device, name="edit_device"),
#	url(r'^manufacturer/(?P<manufacturer_id>[0-9]+)/edit/', views.edit_manufacturer, name="edit_manufacturer"),

#	url(r'^$', views.index, name='index'),
]
