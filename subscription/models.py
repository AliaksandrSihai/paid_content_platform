from django.db import models


class Subscription(models.Model):
    """Creating subscription model"""

    title = models.CharField(max_length=255, verbose_name="title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="price")
    currency = models.CharField(max_length=3, default="EUR", verbose_name="currency")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "subscription"
        verbose_name_plural = "subscriptions"
