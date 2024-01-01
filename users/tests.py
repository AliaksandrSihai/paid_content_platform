from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from subscription.models import Subscription
from users.models import User


class TestUser(TestCase):
    def setUp(self) -> None:
        self.subscription = Subscription.objects.create(
            title="test", price=10, currency="eur"
        )
        self.user = User.objects.create(
            phone="+1234567000",
            password="123qwe456asd",
            subscription=self.subscription,
            email="test@mail.com",
            is_active=True,
        )

    # def test_register(self):
    #     data = {
    #         'phone': "+1234567000",
    #         'email': "test@mail.com",
    #         'password1': '123qwe456asd',
    #         'password2': '123qwe456asd',
    #         'subscription': self.subscription
    #     }
    #     response = self.client.post(reverse('users:register'), data=data)
    #     self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    # def test_register(self):
    #     data = {"phone": "+1234567000", "password": "123qwe456asd"}
    #     response = self.client.post(reverse("users:login"), data=data)
    #     self.assertEqual(response.status_code, status.HTTP_302_FOUND)
