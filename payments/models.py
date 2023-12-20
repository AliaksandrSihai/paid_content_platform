from django.db import models

import users.models
from users.models import NULLABLE


class PaymentModel(models.Model):
    """Creating payments model"""

    payment_date = models.DateTimeField(
        auto_now_add=True, verbose_name="date of payment"
    )
    stripe_id = models.CharField(
        max_length=40, verbose_name="payment id on stripe", **NULLABLE
    )
    payment_status = models.BooleanField(default=False, verbose_name="payment's status")
    user = models.ForeignKey(
        to=users.models.User,
        on_delete=models.DO_NOTHING,
        related_name="user_payment",
        verbose_name="user_payment",
    )

    def __str__(self):
        return f"{self.payment_status}"

    class Meta:
        verbose_name = "payment"
        verbose_name_plural = "payments"
