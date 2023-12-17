from django.contrib import admin
from payments.models import PaymentModel


@admin.register(PaymentModel)
class PaymentModelAdmin(admin.ModelAdmin):
    """Register payments in admin-panel"""

    list_display = ('payment_date', 'payment_status', 'stripe_id')
    list_filter = ('payment_date',)
    ordering = ('payment_date',)
