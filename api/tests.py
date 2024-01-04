from django.test import TestCase
from django.urls import reverse
from posts.models import PostModel
from users.models import User
from rest_framework import status


class ApiTestPost(TestCase):
    """Testing API posts"""

    def setUp(self) -> None:
        self.user = User.objects.create(
            phone="+1234567890",
            password="123qwe456rty",
            is_paid_subscribe=True,
        )
        self.post_1 = PostModel.objects.create(
            title="Post_1", post_owner=self.user, is_free=True
        )
        self.post_2 = PostModel.objects.create(
            title="Post_2",
            description="Test_2 description",
            post_owner=self.user,
            is_free=True,
        )
        self.post_3 = PostModel.objects.create(
            title="Post_3",
            description="Test_3 description",
            post_owner=self.user,
            is_free=False,
        )

    def test_api_list_post(self):
        response_anonim = self.client.get(reverse("api:posts"))
        self.assertEqual(response_anonim.status_code, status.HTTP_200_OK)

        result = response_anonim.json().get("results")
        self.assertEqual(len(result), PostModel.objects.filter(is_free=True).count())

        title = [title["title"] for title in result]
        self.assertIn(self.post_1.title, title)
        self.assertIn(self.post_2.title, title)
        self.assertNotIn(self.post_3.title, title)

        self.client.force_login(self.user)
        response_user = self.client.get(reverse("api:posts"))

        result_all = response_user.json().get("results")
        self.assertEqual(len(result_all), PostModel.objects.all().count())

    def test_api_retrieve_post(self):
        response = self.client.get(reverse("api:post_retrieve", args=[self.post_1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.post_1.title, response.data["title"])
        self.assertNotIn(self.post_2.title, response.data["title"])

    def test_add_like(self):
        self.assertEqual(self.post_1.likes.count(), 0)
        self.client.force_login(self.user)
        response = self.client.post(reverse("api:like_post", args=[self.post_1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post_1.likes.count(), 1)
