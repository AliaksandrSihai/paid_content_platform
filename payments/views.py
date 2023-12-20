import stripe
from django.views import generic
from django.views.generic import View, TemplateView
from payments.forms import PaymentConfirmForm
from payments.models import PaymentModel
from payments.services import confirm_payment, create_payment
from django.urls import reverse_lazy
from django.shortcuts import redirect


class CancelPayment(TemplateView):
    """View for cancel payments"""

    template_name = "payments/cancel.html"


class SuccessPayment(TemplateView):
    """View for success payments"""

    template_name = "payments/success.html"


class ConfirmPayment(generic.FormView):
    model = PaymentModel
    template_name = "payments/confirm_payment.html"
    form_class = PaymentConfirmForm
    success_url = reverse_lazy("posts:all_posts")

    def form_valid(self, form):
        amount = self.request.user.subscription.price
        stripe_payment = create_payment(amount)
        payment = PaymentModel.objects.create(
            user=self.request.user, stripe_id=stripe_payment
        )
        try:
            confirm_payment(
                stripe_id=stripe_payment, receipt_email=self.request.user.email
            )
        except stripe.error.CardError:
            return redirect("payments:cancel")
        else:
            payment.stripe_id = stripe_payment
            payment.payment_status = True
            payment.save()
            self.request.user.is_paid_subscribe = True
            self.request.user.save()
            return redirect("payments:success")

