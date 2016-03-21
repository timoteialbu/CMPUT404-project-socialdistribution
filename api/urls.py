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
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^author/posts/$', views.UserPostList.as_view()),
    url(r'^posts/$', views.PostList.as_view()),
    url(r'^author/(?P<uuid>[^/]+)/posts$', views.AuthorPostList.as_view()),
    url(r'^author/(?P<uuid>[^/]+)/$', views.AuthorDetail.as_view()),
    url(r'^posts/(?P<uuid>[^/]+)/comments$', views.CommentList.as_view(), name='post-comments'),

    url(r'^posts/(?P<uuid>[^/]+)/$', views.PostDetail.as_view()),
    # TODO: Ask the service if author id is friends. In the "authors" include
    # TODO: the 2 authors to compare
    url(r'^friends/(?P<uuid>[^/]+)/$', views.FriendRelationship.as_view()),
    # TODO: Ask the service if anyone in the list is a friend
    # TODO: Similar to above, but in this case the author asking
    # TODO: for this information is in "author" and the "authors" contains a list
    url(r'^friends/(?P<friend1_uuid>[^/]+)/(?P<friend2_uuid>[^/]+)/$', views.FriendsCheck.as_view()),
    # TODO: Make a friend request
    #url(r'^friendrequest/(?P<uuid>[^/]+)/$', views.FriendRequest.as_view()),
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
