from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from posts.forms import PostModelForm
from posts.models import PostModel


class PostListView(generic.ListView):
    """List of all posts"""

    model = PostModel
    ordering = ("publish_date",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated and self.request.user.is_paid_subscribe:
            queryset = PostModel.objects.all()
        else:
            queryset = PostModel.objects.filter(is_free=True)

        queryset = queryset.order_by("-publish_date")
        context["object_list"] = queryset
        return context


class MyPost(LoginRequiredMixin, generic.ListView):
    """List of all posts"""

    model = PostModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = PostModel.objects.filter(post_owner=self.request.user).all()
        queryset = queryset.order_by("-publish_date")
        context["object_list"] = queryset
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    """Create a post"""

    model = PostModel
    form_class = PostModelForm
    success_url = reverse_lazy("posts:all_posts")

    def form_valid(self, form):
        self.object = form.save()
        self.object.post_owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class PostDetailView(generic.DetailView):
    """Getting selected post"""

    model = PostModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["object_list"] = PostModel.objects.filter(pk=self.object.pk)
        else:
            context["object_list"] = PostModel.objects.filter(
                pk=self.object.pk, is_free=True
            )
        self.object.views_count += 1
        self.object.save()
        return context


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Delete selected post"""

    model = PostModel
    success_url = reverse_lazy("posts:all_posts")


class LikedPosts(generic.ListView):
    """All liked posts"""

    model = PostModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = PostModel.objects.filter(likes=self.request.user)
        queryset = queryset.order_by("-publish_date")
        context["object_list"] = queryset
        return context
