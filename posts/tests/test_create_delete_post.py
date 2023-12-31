from django.test import TestCase
from django.urls import reverse
from posts.models import PostModel
from users.models import User
from rest_framework import status


class TestCreateDeletePost(TestCase):
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

    def test_create_post(self):
        self.client.force_login(self.user)
        data = {
            'title': 'Detail_2 Post_2',
            'description': 'Test description',
            'post_owner': self.user,
        }
        posts = PostModel.objects.all()
        self.assertEqual(posts.count(), 1)
        response = self.client.post(reverse('posts:add_post'), data=data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(posts.count(), 2)
        last_post = PostModel.objects.last()
        self.assertEqual(last_post.title, 'Detail_2 Post_2')

    def test_delete_post(self):
        self.client.force_login(self.user)
        post = PostModel.objects.all()
        self.assertEqual(post.count(), 1)
        response = self.client.delete(reverse('posts:delete_post', args=[self.post_1.pk]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(post.count(), 0)