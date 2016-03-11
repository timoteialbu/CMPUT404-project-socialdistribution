from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),


    url(r'^create_post/$', views.create_post, name='create_post'),
    #url(r'^create_img/$', views.create_img, name='create_img'),
    url(r'^post_mgnt/$', views.post_mgnt, name='post_mgnt'),

    url(r'^friend_mgnt/$', views.friend_mgnt, name='friend_mgnt'),

    url(r'^(?P<identity>[^/]+)/$', views.detail, name='detail'),
    
    url(r'^edit_post/(?P<identity>[^/]+)/$',
        views.edit_post, name='edit_post'),

    url(r'^delete_post/(?P<identity>[^/]+)/$',
     views.delete_post, name='delete_post'),

    url(r'^create_img/$', views.create_img, name='create_img'),
]
