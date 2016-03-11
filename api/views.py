from api.models import Post, Author
from api.post_serializers import PostSerializer
from api.post_serializers import AuthorSerializer
from rest_framework import generics, permissions, pagination
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q


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


# TODO FINISH  all, doesnt work (get UUID working with User)
class AuthorPostList(generics.ListAPIView):
    """
    all posts made by {AUTHOR_ID} visible to the currently authenticated user (GET)
    http://service/author/{AUTHOR_ID}/posts 
    """
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        requestId = self.kwargs.get(self.lookup_url_kwarg)
        user = User.objects.filter(Author__uuid=requestId)
        posts = Post.objects.filter(User__pk=user.pk)
        return uuid



class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    access to a single post with id = {POST_ID}
    http://service/posts/{POST_ID} 
    """
    serializer_class = PostSerializer
    # TODO change to something more approp
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        requestId = self.kwargs.get(self.lookup_url_kwarg)
        post = Post.objects.get(identity=requestId)
        print type(requestId)
        print type(Post.objects.values_list('identity', flat=True)[0])
        return post




    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AuthorSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = AuthorSerializer

#####################
# from api.models import Post
# from api.post_serializers import PostSerializer
# from rest_framework import generics


# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


#=========================================================================
# these are equal lol

# from api.models import Post
# from api.post_serializers import PostSerializer
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status


# class PostList(APIView):
#     """
#     List all posts, or create a new post.
#     """
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PostDetail(APIView):
#     """
#     Retrieve, update or delete a post.
#     """
#     def get_object(self, pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
