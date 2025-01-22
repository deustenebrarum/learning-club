from tokenize import Comment
from rest_framework import serializers
from .models import Application, Post, Tag, Topic
from rest_framework.serializers import CurrentUserDefault


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'title', 'description')


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    tags = serializers.SerializerMethodField('get_tags')
    
    def get_tags(self, obj):
        return TagSerializer(obj.tags.all(), many=True).data

    class Meta:
        model = Post
        fields = (
            'id', 'user_id', 'user', 'tags', 'title', 'content', 'topic_id',
            'created_at', 'updated_at'
        )
        read_only_fields = ('user_id', 'created_at', 'updated_at')


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'application_type', 'application_file')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Comment
        fields = (
            'id', 'user_id', 'user', 'post_id',
            'content', 'created_at', 'updated_at'
        )
        read_only_fields = ('user_id', 'created_at', 'updated_at')

    def user_id(self, obj):
        return obj.user.id
