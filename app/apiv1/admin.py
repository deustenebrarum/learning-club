from django.contrib import admin

from .models import (
    Application, Post, Comment,
    Topic, Tag
)

admin.site.register(Application)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'topic',
                    'created_at', 'updated_at')
    list_display_links = ('id', 'user', 'topic')
    search_fields = ('user__username', 'content',
                     'topic__title', 'tags__title')
    list_filter = ('topic', 'tags', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'content',
                    'created_at', 'updated_at')
    list_display_links = ('id', 'post', 'user')
    search_fields = ('post__content', 'user__username',
                     'content')
    list_filter = ('post__topic', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
