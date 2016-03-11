from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_post/$', views.create_post, name='create_post'),
    url(r'^(?P<identity>[^/]+)/$', views.detail, name='detail'),
    url(r'^edit_post/(?P<identity>[^/]+)/$',
        views.edit_post, name='edit_post'),

    #url(r'^(?P<post_id>[0-9]+)/$', views.delete_post, name='delete_post'),
    url(r'^delete_post/(?P<identity>[^/]+)/$',
     views.delete_post, name='delete_post'),

    # I added this function and it locates in views line 195
    url(r'^post_mgnt/$', views.post_mgnt, name='post_mgnt'),

    url(r'^create_img/$', views.create_img, name='create_img'),
    # url(r'^edit_img/(?P<post_id>[0-9]+)/$', views.edit_img, name='edit_img'),

    url(r'^friend_mgnt/$', views.friend_mgnt, name='friend_mgnt'),
]
