from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from config.settings import STRIPE_WEBHOOK_KEY
from payments.models import PaymentModel
from subscription.models import Subscription
from users.models import User


class ConfirmPaymentTest(TestCase):
    def setUp(self) -> None:
        self.subscription = Subscription.objects.create(
            title="test",
            price=10,
            currency="eur",
        )
        self.subscription.save()
        self.user = User.objects.create(phone="+1234567890", password="123qwe456asd")

        self.payment = PaymentModel.objects.create(
            user=self.user,
            subscription=self.subscription,
        )
        self.url = reverse("payments:confirm")

    def test_confirm_payment_view(self):
        self.client.force_login(self.user)
        self.assertFalse(self.user.is_paid_subscribe)
        form_data = {"subscription": self.subscription.id}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertIn("checkout.stripe.com", response.url)

    @patch("stripe.Webhook.construct_event")
    def test_webhook_view(self, mock_construct_event):
        self.client.force_login(self.user)
        mock_construct_event.return_value = {
            "type": "payment_intent.succeeded",
            "data": {"object": {"metadata": {"payment_id": 1}}},
        }

        url = "http://localhost:8000/webhook/stripe/"

        response = self.client.post(
            url,
            data='{"key": "value"}',
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=STRIPE_WEBHOOK_KEY,
        )

        self.assertEqual(response.status_code, 200)
