from django.test import TestCase
from django.urls import reverse

from subscription.models import Subscription
from users.models import User


# Create your tests here.
class TestUser(TestCase):
    def setUp(self) -> None:
        self.subscription = Subscription.objects.create(
            title='test',
            price=10,
            currency='eur'
        )
        self.user = User.objects.create(
            phone="+1234567890",
            password='123qwe456asd',
            subscription=self.subscription
        )

    def test_register(self):
        # self.assertFalse(self.client.user.is_authenticated)
        # self.client.login()
        data = {
            'phone': "+1234567890",
            'email': "test@mail.ru",
            'password1': '123qwe456asd',
            'password2': '123qwe456asd',
            'subscription': self.subscription
        }
        response = self.client.post(reverse('users:register'), data=data)
        print(response.status_code)
