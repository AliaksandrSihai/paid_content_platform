from django.urls import path

from api.apps import ApiConfig
from api.views import AddLikeView, AllPosts, Post

app_name = ApiConfig.name

urlpatterns = [
    path("v1/posts/", AllPosts.as_view(), name="posts"),
    path("v1/post/<int:pk>/", Post.as_view(), name="post_retrieve"),
    path("v1/like_post/<int:pk>/", AddLikeView.as_view(), name="like_post"),
]
