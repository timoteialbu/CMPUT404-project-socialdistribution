from api.models import *
from api.serializers import *
from rest_framework import generics, permissions, pagination
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
import uuid


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
        return Post.objects.filter(identity=postId)

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


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = AuthorSerializer
