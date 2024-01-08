from django.urls import path

from posts import views
from posts.apps import PostsConfig

app_name = PostsConfig.name

urlpatterns = [
    path("", views.PostListView.as_view(), name="all_posts"),
    path("my_posts/", views.MyPost.as_view(), name="my_posts"),
    path("add_post/", views.PostCreateView.as_view(), name="add_post"),
    path("post/<int:pk>", views.PostDetailView.as_view(), name="post"),
    path("delete_post/<int:pk>", views.PostDeleteView.as_view(), name="delete_post"),
    path("liked_post/", views.LikedPosts.as_view(), name="liked_posts"),
]
