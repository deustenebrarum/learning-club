from .models import Application, Post, Tag, Topic, Comment
from .serializers import (
    ApplicationSerializer, CommentSerializer, PostSerializer,
    TagSerializer, TopicSerializer
)
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticatedOrReadOnly
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class TopicViewSet(ModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['topic_id']
    search_fields = ['title', 'content', 'tags__title', 'topic__title']
    ordering_fields = ['created_at', 'updated_at']


class ApplicationViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['post_id']
    ordering_fields = ['created_at', 'updated_at']
