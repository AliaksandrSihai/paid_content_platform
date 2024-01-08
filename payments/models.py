from django.db import models

from subscription.models import Subscription
from users.models import NULLABLE, User


class PaymentModel(models.Model):
    """Creating payments model"""

    payment_date = models.DateTimeField(
        auto_now_add=True, verbose_name="date of payment"
    )
    stripe_id = models.CharField(
        max_length=128, verbose_name="payment id on stripe", **NULLABLE
    )
    payment_status = models.BooleanField(default=False, verbose_name="payment's status")
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
        related_name="user_payment",
        verbose_name="user_payment",
        **NULLABLE,
    )
    subscription = models.ForeignKey(
        to=Subscription, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.payment_status}"

    class Meta:
        verbose_name = "payment"
        verbose_name_plural = "payments"
