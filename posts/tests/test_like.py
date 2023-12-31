from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from posts.models import PostModel
from users.models import User


class LikeTest(TestCase):
    def setUp(self) -> None:
        self.user_1 = User.objects.create(phone="+1234567890", password="123qwe456rty")
        self.user_2 = User.objects.create(phone="+1234500000", password="123qwe456rty")

        self.post = PostModel.objects.create(
            title="Post", description="Test description", post_owner=self.user_1
        )

    def test_liked_posts(self):
        self.client.force_login(self.user_2)
        response = self.client.get(reverse("posts:liked_posts"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        like = PostModel.objects.filter(likes=self.user_2).count()
        self.assertEqual(like, 0)
        self.assertNotIn(self.post.title, response.content.decode("utf-8"))

        self.client.post(reverse("api:like_post", args=[self.post.pk]))
        self.post.refresh_from_db()
        liked_post = PostModel.objects.filter(likes=self.user_2).count()
        self.assertEqual(liked_post, 1)
