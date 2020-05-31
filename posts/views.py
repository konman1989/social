from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     GenericAPIView,
                                     ListAPIView)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .filters import LikesFilter
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer
from .permissions import IsOwner
from users.serializers import UserSerializer


class PostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class PostLikeView(ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = Post.objects.get(pk=pk).likes
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        author = self.request.user
        pk = kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        post.likes.add(author)
        serializer = self.get_serializer(
            data={'author': author.pk, 'post': pk})
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def delete(self, request, **kwargs):
        author = request.user
        pk = kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        post.likes.remove(author)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikesAnalyticsView(ListAPIView):
    queryset = Like.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LikesFilter


