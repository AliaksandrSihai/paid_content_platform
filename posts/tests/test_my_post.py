from django.test import TestCase
from django.urls import reverse
from posts.models import PostModel
from users.models import User
from rest_framework import status


class TestMyPost(TestCase):
    def setUp(self) -> None:
        self.user_1 = User.objects.create(phone="+1234567890", password="123qwe456asd")
        self.user_2 = User.objects.create(phone="+9876543210", password="123qwe456asd")
        self.post_1 = PostModel.objects.create(title="Post_1", post_owner=self.user_1)
        self.post_2 = PostModel.objects.create(
            title="Post_2", description="Test description", post_owner=self.user_2
        )

    def test_my_post(self):
        self.client.force_login(self.user_1)
        response = self.client.get(reverse("posts:my_posts"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.post_1.title, response.content.decode("utf-8"))
        self.assertNotIn(self.post_2.title, response.content.decode("utf-8"))
