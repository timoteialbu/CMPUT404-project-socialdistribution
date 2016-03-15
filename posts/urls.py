from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^create_img/$', views.create_img, name='create_img'),
    
    url(r'^$', views.index, name='index'),

    #url(r'^create_img/$', views.create_img, name='create_img'),
    url(r'^post_mgnt/$', views.post_mgnt, name='post_mgnt'),

    url(r'^friend_mgnt/$', views.friend_mgnt, name='friend_mgnt'),

    url(r'^(?P<identity>[^/]+)/$', views.post_detail, name='detail'),



    url(r'^(?P<identity>[^/]+)$', views.delete_post, name='delete_post'),

        
]
