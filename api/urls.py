from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from api import views


# Maybe delete
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# Maybe delete
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Maybe delete
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include(
        'rest_framework.urls',
        namespace='rest_framework')
        ),
    url(r'^author/posts/$', views.UserPostList.as_view()),
    url(r'^posts/$', views.PostList.as_view()),
    url(r'^author/(?P<uuid>[^/]+)/posts$', views.AuthorPostList.as_view()),
    url(r'^posts/(?P<uuid>[^/]+)/$', views.PostDetail.as_view()),
    # url(r'^author/$', views.UserList.as_view()),
    # url(r'^author/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

# Catch-alls, to be added to the end of the URL
# load order might catch mishandled queries
# MUST have a / at the end also.
# Eg. r'^.*/$' instead of r'^.*' as last pattern.
# To pass url to view AS A NAMED ARG, use r'^(?P<url>.*)/$'.


# adds extra suffix patterns to urls might be good for pagination
# urlpatterns = format_suffix_patterns(urlpatterns)
