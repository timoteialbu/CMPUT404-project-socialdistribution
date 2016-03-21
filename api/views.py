from api.models import *
from api.serializers import *
from rest_framework import generics, permissions, pagination
from rest_framework.response import Response
from django.contrib.auth.models import User
from friendship.models import Friend
from django.db.models import Q
import uuid
import copy


class UserPostList(generics.ListAPIView):
    """
    posts that are visible to the currently authenticated user (GET)
    http://service/author/posts 
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        """
        This view should return a list of all the posts
        that are visible to the currently authenticated user
        """
        # TODO add friend logic
        posts = Post.objects.filter(
            Q(visibility='PUBLIC') |
            Q(author=Author.objects.get(user=self.request.user)))
        return posts


class PostList(generics.ListCreateAPIView):
    """
    List all Public Posts on the server(GET)
    http://service/posts
    """
    queryset = Post.objects.filter(visibility='PUBLIC')
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save(author=Author.objects.get(user=self.request.user))


class AuthorPostList(generics.ListAPIView):
    """
    all posts made by {AUTHOR_ID} visible to the currently authenticated user (GET)
    http://service/author/{AUTHOR_ID}/posts 
    """
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        authorId = self.kwargs.get(self.lookup_url_kwarg)
        posts = Post.objects.filter(
            Q(author=authorId),
            Q(visibility='PUBLIC') | Q(author__user=self.request.user)
        )  # TODO needs friend logic
        return posts


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    access to a single post with id = {POST_ID}
    http://service/posts/{POST_ID}
    """
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        postId = self.kwargs.get(self.lookup_url_kwarg)
        return Post.objects.filter(id=postId)


    def perform_create(self, serializer_class):
        author = Author.objects.filter(user=self.request.user)
        serializer_class.save(author=author)


class CommentList(generics.ListAPIView):
    """
    access to the comments in a post
    http://service/posts/{post_id}/comments access to the comments in a post
    """
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        postId = self.kwargs.get(self.lookup_url_kwarg)
        return Comment.objects.filter(post=postId)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AuthorSerializer


#class UserDetail(generics.RetrieveAPIView):
#    queryset = User.objects.all()
#    serializer_class = AuthorSerializer

class AuthorDetail(generics.RetrieveAPIView):
    serializer_class = AuthorSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        authorId = self.kwargs.get(self.lookup_url_kwarg)
        return Author.objects.filter(id=authorId)


class FriendRelationship(generics.ListCreateAPIView):
    """
    Returns your friend relationship with a certain author
    http://service/friends/(?P<uuid>[^/]+)
    """
    queryset = Author.objects.all()
    serializer_class = FriendSerializer

    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        # Get the uuid from the url
        request_id = self.kwargs.get(self.lookup_url_kwarg)
        # Find the author object with that uuid
        username = Author.objects.get(id=request_id)
        # Get all the friends
        all_friends = Friend.objects.friends(username.user)
        # Get the authors objects version of those friends objects
        all_authors = Author.objects.filter(user__in=all_friends)
        return all_authors


class FriendsCheck(generics.ListCreateAPIView):
    """
    Returns your friend relationship with a certain author
    http://service/friends/(?P<uuid>[^/]+)/(?P<uuid>[^/]+)
    """
    queryset = Author.objects.all()
    serializer_class = FriendsCheckSerializer()

    lookup_url_kwarg_1 = 'friend1_uuid'
    lookup_url_kwarg_2 = 'friend2_uuid'

    def get_queryset(self):
        # Get the uuid from the url
        request_id_1 = self.kwargs.get(self.lookup_url_kwarg_1)
        request_id_2 = self.kwargs.get(self.lookup_url_kwarg_2)
        # Find the author object with that uuid
        username_1 = Author.objects.get(id=request_id_1)
        username_2 = Author.objects.get(id=request_id_2)
        # Check if friends
        result = Friend.objects.are_friends(username_1.user, username_2.user)
        authors2 = list()
        authors2.append(request_id_1)
        authors2.append(request_id_2)
        friend_pair = FriendsPair(authors2, result)
        resultlist = list()
        resultlist.append(friend_pair)
        return resultlist
