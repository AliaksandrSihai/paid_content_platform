from django.db import models
from subscription.models import Subscription
from users.models import NULLABLE


class PaymentModel(models.Model):
    """Creating payments model"""

    subscription = models.ForeignKey(to=Subscription, on_delete=models.DO_NOTHING, related_name='subscription',
                                     verbose_name='subscription')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='date of payment')
    stripe_id = models.CharField(max_length=40, verbose_name='payment id on stripe', **NULLABLE)
    payment_status = models.BooleanField(default=False, verbose_name="payment's status")

    def __str__(self):
        return f'{self.payment_status}'

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
