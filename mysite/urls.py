from django.conf.urls import patterns, include, url
from django.contrib import admin
from mysite.views import Index

admin.autodiscover()  ##according to the django tut (1.8) this shouldnt be here? idk

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', Index.as_view(), name='index'),
                       url(r'^posts/', include('posts.urls', namespace="posts")),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/', include('allauth.urls')),
)



