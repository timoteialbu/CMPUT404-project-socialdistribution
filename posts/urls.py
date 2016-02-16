from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_post/$', views.create_post, name='create_post'),
    url(r'^(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^edit_post/(?P<post_id>[0-9]+)/$', views.edit_post, name='edit_post'),


    url(r'^create_img/$', views.create_img, name='create_img'),
    url(r'^edit_img/(?P<post_id>[0-9]+)/$', views.edit_img, name='edit_img'),


]

