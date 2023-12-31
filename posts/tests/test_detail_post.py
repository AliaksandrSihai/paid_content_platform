from django.test import TestCase, Client
from posts.models import PostModel
from users.models import User
from django.urls import reverse
from rest_framework import status


class TestPostDetailView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            phone='1234567890',
            password='123qwe456ert'
        )
        self.post_1 = PostModel.objects.create(
            title='Detail Post',
            post_owner=self.user,
            is_free=True
        )
        self.post_2 = PostModel.objects.create(
            title='Detail_2 Post_2',
            post_owner=self.user,
            is_free=True
        )

    def test_detail_post(self):
        response = self.client.get(reverse('posts:post', args=[self.post_1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.post_1.title, response.content.decode('utf-8'))
        self.assertNotIn(self.post_2.title, response.content.decode('utf-8'))
