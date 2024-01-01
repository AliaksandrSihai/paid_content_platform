from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from posts.forms import PostModelForm
from posts.models import PostModel


class PostListView(generic.ListView):
    """List of all posts"""

    model = PostModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.is_paid_subscribe:
            context["object_list"] = PostModel.objects.all()
        else:
            context["object_list"] = PostModel.objects.filter(is_free=True).all()
        return context


class MyPost(LoginRequiredMixin, generic.ListView):
    """List of all posts"""

    model = PostModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = PostModel.objects.filter(post_owner=self.request.user).all()
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


@login_required
def like_post(request, pk):
    post = get_object_or_404(PostModel, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})

