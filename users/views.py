from rest_framework import status
from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .permissions import IsOwner
from .serializers import (UserSerializer,
                          UserActivitySerializer,
                          CreateUserSerializer,
                          CustomTokenSerializer)
from posts.models import Like
from posts.serializers import (PostSerializer,
                               LikeSerializer,)


class UsersView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['email', 'first_name', 'last_name']


class UserCreateView(CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        refresh = RefreshToken.for_user(instance)
        data = serializer.data
        data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        headers = self.get_success_headers(data)
        return Response(data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class UserDetailActivityView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        query = self.request.query_params.get('query')
        if query == 'posts':
            author = self.get_object()
            serializer = PostSerializer(author.posts.all(), many=True)
            return Response(serializer.data)
        if query == 'likes':
            like = Like.objects.filter(author=self.get_object())
            serializer = LikeSerializer(like, many=True)
            return Response(serializer.data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)




