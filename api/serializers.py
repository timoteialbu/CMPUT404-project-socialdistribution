from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Post, Author, Comment, Friends, FriendsPair
from friendship.models import Friend


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('uuid', 'host', 'displayName', 'url', 'github')


class CommentSerializer(serializers.ModelSerializer):
    # author = AuthorSerializer(source='author')
    class Meta:
        model = Comment
        fields = ('comment', 'contentType', 'published', 'id',)

class UserSerializer(serializers.ModelSerializer):
    #userinfo = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    author = AuthorSerializer(source='author')
    class Meta:
        model = User
        fields = ('author',)

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ('uuid',)


class FriendsCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendsPair
        fields = ('authors', 'friends',)

     
class PostSerializer(serializers.ModelSerializer):
    # TODO change source to = some user serializer with ID, host,displayname
    # url and github (see api protocols)
    author = AuthorSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)

    
    class Meta:
        model = Post
        fields = (
            'title', 'source', 'origin', 'description',
            'contentType', 'content', 'author', 'categories',
            'published', 'identity', 'visibility', 'comment',
        )


















