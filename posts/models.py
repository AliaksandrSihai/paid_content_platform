from django.db import models

import users.models
from users.models import NULLABLE


class PostModel(models.Model):
    """Post's model"""
    title = models.CharField(max_length=255, verbose_name='title')
    description = models.TextField(verbose_name='description', **NULLABLE)
    post_owner = models.ForeignKey(to=users.models.User, on_delete=models.CASCADE,
                                   related_name='post_owner', verbose_name='post_owner')
    is_free = models.BooleanField(default=False, verbose_name="post's status")
    image = models.ImageField(upload_to='posts/', verbose_name='avatar', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
