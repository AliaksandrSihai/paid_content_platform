from django.db import models
from config.settings import AUTH_USER_MODEL
import users.models
from users.models import NULLABLE


class PostModel(models.Model):
    """Post's model"""

    title = models.CharField(max_length=255, verbose_name="title")
    description = models.TextField(verbose_name="description", **NULLABLE)
    post_owner = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_owner",
                                   verbose_name="post_owner", null=True)
    is_free = models.BooleanField(default=False, verbose_name="is free?")
    image = models.ImageField(upload_to="posts/", verbose_name="image", **NULLABLE)
    publish_date = models.DateField(auto_now_add=True, verbose_name="published date")
    likes = models.ManyToManyField(
        to=users.models.User, related_name="likes", default=0
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
