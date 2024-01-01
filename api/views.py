from rest_framework.generics import ListAPIView, RetrieveAPIView
from api.serializers import PostSerializer
from posts.models import PostModel
from api.paginators import ListPaginator


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
