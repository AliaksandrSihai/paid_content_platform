from django.shortcuts import get_object_or_404
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     RetrieveAPIView)
from rest_framework.response import Response

from api.paginators import ListPaginator
from api.serializers import PostSerializer
from posts.models import PostModel


class AllPosts(ListAPIView):
    """Api for all posts"""

    serializer_class = PostSerializer
    pagination_class = ListPaginator

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = PostModel.objects.all()

        else:
            queryset = PostModel.objects.filter(is_free=True)

        return queryset


class Post(RetrieveAPIView):
    """Api for one post"""

    serializer_class = PostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = PostModel.objects.all()
        else:
            queryset = PostModel.objects.filter(is_free=True)

        return queryset


class AddLikeView(GenericAPIView):
    def post(self, request, pk):
        post = get_object_or_404(PostModel, pk=pk)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return Response({"liked": liked, "likes_count": post.likes.count()})
