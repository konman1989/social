from django.urls import path

from . import views

app_name = 'users_api'

urlpatterns = [
    path('', views.UsersView.as_view(), name='users'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/activity/', views.UserDetailActivityView.as_view(),
         name='user_activity'),
]
