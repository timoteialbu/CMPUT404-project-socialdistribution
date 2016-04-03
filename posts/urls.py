from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),

    url(r'^create_img/$', views.create_img, name='create_img'),

    url(r'^post_mgmt/$', views.post_mgmt, name='post_mgmt'),

    url(r'^friend_mgmt/$', views.friend_mgmt, name='friend_mgmt'),

    url(r'^nodes/$', views.get_nodes, name='get_nodes'),

    url(r'^profile/$', views.get_profile, name='update_profile'),

    url(r'^(?P<id>[^/]+)/$', views.get_post_detail, name='detail'),

    url(r'^(?P<id>[^/]+)$', views.delete_post, name='delete_post'),

]
