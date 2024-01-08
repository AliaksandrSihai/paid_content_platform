from http import HTTPStatus

import stripe
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from config.settings import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_KEY, DOMAIN_NAME
from payments.forms import PaymentForm
from payments.models import PaymentModel
from subscription.models import Subscription
from users.models import User

stripe.api_key = STRIPE_SECRET_KEY


class CancelPayment(TemplateView):
    """View for cancel payments"""

    template_name = "payments/cancel.html"


class SuccessPayment(TemplateView):
    """View for success payments"""

    template_name = "payments/success.html"


class ConfirmPayment(generic.CreateView):
    model = PaymentModel
    template_name = "payments/confirm_payment.html"
    form_class = PaymentForm
    success_url = reverse_lazy("posts:all_posts")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        payment_instance = Subscription.objects.get(pk=int(form.data["subscription"]))
        super(ConfirmPayment, self).post(request, *args, **kwargs)
        price = payment_instance.stripe_price_id
        session = stripe.checkout.Session.create(
            success_url=DOMAIN_NAME + reverse("payments:success"),
            line_items=[{"price": price, "quantity": 1}],
            mode="payment",
            metadata={"payment_id": self.object.id},
        )
        return HttpResponseRedirect(session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ConfirmPayment, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_KEY)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    if event["type"] == "checkout.session.completed":
        session = stripe.checkout.Session.retrieve(event["data"]["object"]["id"])

        fulfill_order(session)

    return HttpResponse(status=200)


def fulfill_order(session):
    payment_id = int(session.metadata.payment_id)
    payment = PaymentModel.objects.get(pk=payment_id)
    payment.payment_status = True
    payment.stripe_id = session.stripe_id
    payment.save()

    user = User.objects.get(pk=payment.user.pk)
    user.is_paid_subscribe = True
    user.save()
