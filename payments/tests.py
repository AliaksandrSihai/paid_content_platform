from django.test import TestCase
from django.urls import reverse
from payments.models import PaymentModel
from subscription.models import Subscription
from users.models import User
from rest_framework import status


class ConfirmPaymentTest(TestCase):
    def setUp(self) -> None:
        self.subscription = Subscription.objects.create(
            title="test", price=10, currency="eur"
        )
        self.user = User.objects.create(
            phone="+1234567890", password="123qwe456asd", subscription=self.subscription
        )

        self.data = {
            "card_number": 123456789012,
            "exp_month": "12",
            "exp_year": "25",
            "cvc": "999",
            "name": "Test Testov",
        }
        self.url = reverse("payments:confirm")

    def test_confirm_payment_view(self):
        self.client.force_login(self.user)
        self.assertFalse(self.user.is_paid_subscribe)

        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("payments:success"))

        payment = PaymentModel.objects.get(user=self.user)
        self.assertTrue(payment.payment_status)

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_paid_subscribe)
