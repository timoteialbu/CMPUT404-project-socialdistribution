from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^createPost/$', views.create_post, name='create_post'),
   
    ##### snagged from django tut1.8, using as example
    # ex: /polls/5/
    url(r'^(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^edit_post/(?P<post_id>[0-9]+)/$', views.edit_post, name='edit_post'),

    # ex: /polls/5/results/
#    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
#    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    ###################################################s

]

