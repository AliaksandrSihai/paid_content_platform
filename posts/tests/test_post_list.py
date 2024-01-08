from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from posts.models import PostModel
from users.models import User


class TestPost(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            phone="+1234567890",
            password="123qwe456asd",
        )
        self.post_1 = PostModel.objects.create(title="Post_1", post_owner=self.user)
        self.post_2 = PostModel.objects.create(
            title="Post_2", description="Test description", post_owner=self.user
        )

    def test_post_list_view(self):
        response = self.client.get(reverse("posts:all_posts"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PostModel.objects.count(), 2)
        post = PostModel.objects.last()
        self.assertEqual(post.title, "Post_2")
        self.assertEqual(post.description, "Test description")
