from rest_framework import serializers

from .models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    content = serializers.CharField(error_messages={
        'required': 'Argument is either missing or wrong.',
        'blank': 'This field cannot be empty.'
    })

    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['pk', 'content', 'created_on', 'author']


class LikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['post', 'liked_on', 'author']






