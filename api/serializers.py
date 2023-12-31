from rest_framework.serializers import ModelSerializer, SerializerMethodField

from posts.models import PostModel


class PostSerializer(ModelSerializer):
    """Serializer for model PostModel"""
    # like = SerializerMethodField(read_only=True)
    #
    # def get_like(self, instance):
    #     return instance.likes.count()

    class Meta:
        model = PostModel
        fields = '__all__'
        # exclude = ('likes',)
