from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Post, Author, Comment
from friendship.models import Friend
from api.pagination import CustomPagination
from rest_framework import pagination, serializers
import socket
from django.core.urlresolvers import reverse

try:
    HOSTNAME = socket.gethostname()
except:
    HOSTNAME = 'localhost:8000'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'host', 'displayName', 'url', 'github')


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('author', 'comment', 'contentType', 'published', 'id',)


class UserSerializer(serializers.ModelSerializer):
    # userinfo = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    author = AuthorSerializer(source='author')

    class Meta:
        model = User
        fields = ('author',)


class PostSerializer(serializers.HyperlinkedModelSerializer):
    # TODO change source to = some user serializer with ID, host,displayname
    # url and github (see api protocols)
    author = AuthorSerializer(read_only=True)
    # comments = Comment.objects.all()
    # comment_set = CommentSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField('paginated_comments')
    # comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    count = serializers.SerializerMethodField('comment_count')
    size = serializers.SerializerMethodField('comment_size')
    next = serializers.SerializerMethodField('next_page')
    query = serializers.SerializerMethodField('query_type')

    class Meta:
        model = Post
        fields = (
            'title', 'source', 'origin', 'description',
            'contentType', 'content', 'author', 'categories',
            'count', 'size', 'next',
            'comments', 'published', 'id', 'visibility', 'query',

        )

        depth = 1

    def paginated_comments(self, obj):
        comments = Comment.objects.filter(post=obj)[:5]  # [:5]
        paginator = CustomPagination()
        page = paginator.paginate_queryset(comments, self.context['request'])
        serializer = CommentSerializer(page, many=True, context={'request': self.context['request']})
        return serializer.data

    def comment_count(self, obj):
        return len(Comment.objects.filter(post=obj))

    def comment_size(self, obj):
        return 5

    def next_page(self, obj):
        id = str(obj.id)
        uri = reverse('post-comments', kwargs={'uuid': id})
        uri = self.context['request'].build_absolute_uri(uri)
        if self.comment_count(obj) > 5:
            uri = uri + "?page=2"
        else:
            uri = None
        return uri

    def query_type(self, obj):
        return 'posts'
