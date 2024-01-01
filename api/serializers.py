from rest_framework.serializers import ModelSerializer

from posts.models import PostModel


class PostSerializer(ModelSerializer):
    """Serializer for model PostModel"""

    class Meta:
        model = PostModel
        fields = "__all__"
