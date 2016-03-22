from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),

    url(r'^create_img/$', views.create_img, name='create_img'),

    url(r'^post_mgnt/$', views.post_mgnt, name='post_mgnt'),

    url(r'^friend_mgnt/$', views.friend_mgnt, name='friend_mgnt'),

    url(r'^nodes/$', views.nodes, name='nodes'),

    url(r'^profile/$', views.get_profile, name='update_profile'),

    url(r'^(?P<id>[^/]+)/$', views.post_detail, name='detail'),

    url(r'^(?P<id>[^/]+)$', views.delete_post, name='delete_post'),

]
