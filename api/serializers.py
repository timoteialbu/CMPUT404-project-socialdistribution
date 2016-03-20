from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Post, Author, Comment, Friends, FriendsPair
from friendship.models import Friend
from rest_framework import pagination


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

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ('id',)



class FriendsCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendsPair
        fields = ('authors', 'friends',)



class PostSerializer(serializers.ModelSerializer):
    # TODO change source to = some user serializer with ID, host,displayname
    # url and github (see api protocols)
    author = AuthorSerializer(read_only=True)
    # comment = CommentSerializer(many=True, read_only=False)
    comments = serializers.SerializerMethodField('paginated_comments')
    # comment = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    count = serializers.SerializerMethodField('comment_count')
    # next = serializers.SerializerMethodField('next_page')
    size = serializers.SerializerMethodField('comment_size')
    next = serializers.SerializerMethodField('next_page')
    query = serializers.SerializerMethodField('query_type')


    class Meta:
        model = Post
        fields = (
            'query', 'title', 'source', 'origin', 'description',
            'contentType', 'content', 'author', 'categories',
            'count', 'size', 'next',
            'comments', 'published', 'id', 'visibility',

        )

    def paginated_comments(self, obj):
        comments = Comment.objects.filter(post=obj)  # [:5]
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(comments, self.context['request'])
        serializer = CommentSerializer(
            page,
            many=True,
            context={'request': self.context['request']}
        )
        return serializer.data

    def next_page(self, obj):
        print "not complete"
        # if not self.Paginated_comments.has_next():
        #    return None
        # page_number = self.page.next_page_number()
        # return replace_query_param('', self.page_query_param, page_number)

    def comment_count(self, obj):
        return len(Comment.objects.filter(post=obj))

    def comment_size(self, obj):
        return 5

    def query_type(self, obj):
        return 'posts'
