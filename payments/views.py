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
    template_name = 'payments/cancel.html'


class SuccessPayment(TemplateView):
    """View for success payments"""
    template_name = 'payments/success.html'


class ConfirmPayment(generic.FormView):
    model = PaymentModel
    template_name = 'payments/confirm_payment.html'
    form_class = PaymentConfirmForm
    success_url = reverse_lazy('posts:all_posts')

    def form_valid(self, form):
        amount = self.request.user.subscription.price
        stripe_payment = create_payment(amount)
        payment = PaymentModel.objects.create(user=self.request.user,
                                              stripe_id=stripe_payment)
        try:
            confirm_payment(
                            stripe_id=stripe_payment,
                            receipt_email=self.request.user.email)
        except stripe.error.CardError:
            return redirect('payments:cancel')
        else:
            payment.stripe_id = stripe_payment
            payment.payment_status = True
            payment.save()
            self.request.user.is_paid_subscribe = True
            self.request.user.save()
            return redirect('payments:success')


# def payment_view(request):
#     if request.method == 'POST':
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             number = form.cleaned_data['card_number']
#             exp_month = form.cleaned_data['exp_month']
#             exp_year = form.cleaned_data['exp_year']
#             cvc = form.cleaned_data['cvc']
#             name = form.cleaned_data['name']
#
#             # Вызов функции payment_card
#             payment_method_id = payment_card(number, exp_month, exp_year, cvc, name)
#
#             return HttpResponse(f'Success! Payment Method ID: {payment_method_id}')
#     else:
#         form = PaymentForm()
#
#     return render(request, 'payment_form.html', {'form': form})