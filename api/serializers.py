from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Post, Author, Comment


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('uuid', 'host', 'displayName', 'url', 'github')


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('author', 'comment', 'contentType', 'published', 'id',)

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
#         fields = ('id', 'username', 'posts')

     
class PostSerializer(serializers.ModelSerializer):
    # TODO change source to = some user serializer with ID, host,displayname
    # url and github (see api protocols)
    author = AuthorSerializer(read_only=True)
    comment = CommentSerializer(many=True, read_only=False)
    # comment = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author =Author.objects.filter(uuid=author_data["uuid"])
        post = Post.objects.create(author=author, **validated_data)
        post = setid(post)
        return post

    def setid(self, post_data):
        post_data['id'] = post['id']
        post_data.pop('id', None)
        return post_data

    class Meta:
        model = Post
        fields = (
            'title', 'source', 'origin', 'description',
            'contentType', 'content', 'author', 'categories',
            'comment', 'published', 'id', 'visibility',
        )


















