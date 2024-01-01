from api.apps import ApiConfig
from django.urls import path
from api.views import AllPosts, Post

app_name = ApiConfig.name

urlpatterns = [
    path("v1/posts/", AllPosts.as_view(), name="posts"),
    path("v1/post/<int:pk>/", Post.as_view(), name="post_retrieve"),
]
