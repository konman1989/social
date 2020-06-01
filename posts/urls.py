from django.urls import path

from . import views

app_name = 'posts_api'

urlpatterns = [
    path('', views.PostView.as_view(), name='posts'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/likes/', views.PostLikeView.as_view(), name='post_likes'),
    path('analytics/', views.PostLikesAnalyticsView.as_view(),
         name='post_likes'),
]
