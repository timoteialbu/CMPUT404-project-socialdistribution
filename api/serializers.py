from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Post, Author, Comment
from django.core.paginator import Paginator
from rest_framework import pagination

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('uuid', 'host', 'displayName', 'url', 'github')


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('author', 'comment', 'contentType', 'published', 'identity',)

class UserSerializer(serializers.ModelSerializer):
    #userinfo = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    author = AuthorSerializer(source='author')
    class Meta:
        model = User
        fields = ('author')


# class AuthorSerializer(serializers.ModelSerializer):
#     posts = serializers.PrimaryKeyRelatedField(
#         many=True, queryset=Post.objects.all())

#     class Meta:
#         model = User
#         fields = ('identity', 'username', 'posts')


class PostSerializer(serializers.ModelSerializer):
    # TODO change source to = some user serializer with ID, host,displayname
    # url and github (see api protocols)
    author = AuthorSerializer(read_only=True)
    # comment = CommentSerializer(many=True, read_only=False)
    comment = serializers.SerializerMethodField('paginated_comments')
    # comment = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'title', 'source', 'origin', 'description',
            'contentType', 'content', 'author', 'categories',
            'comment', 'published', 'identity', 'visibility',
        )

    def paginated_comments(self, obj):
        comments = Comment.objects.filter(post=obj)[:5]
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(comments, self.context['request'])
        serializer = CommentSerializer(page, many=True, context={'request': self.context['request']})
        return serializer.data

















