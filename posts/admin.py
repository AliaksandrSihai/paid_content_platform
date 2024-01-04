from django.contrib import admin
from posts.models import PostModel


@admin.register(PostModel)
class PostModelAdmin(admin.ModelAdmin):
    """Register post in admin-panel"""

    list_display = ("post_owner", "title", "is_free", "publish_date")
    list_filter = ("post_owner", "title")
    ordering = ("publish_date",)
