import stripe
from config.settings import STRIPE_SECRET_KEY
from django.urls import reverse


stripe.api_key = STRIPE_SECRET_KEY


def create_payment(amount):
    """ Create PaymentIntent """
    amount_stripe = int((amount * 100))
    secret = stripe.PaymentIntent.create(
        amount=amount_stripe,
        currency="eur",
        setup_future_usage='off_session',
        payment_method_types=['card'],
    )
    return secret.id


def confirm_payment(stripe_id, receipt_email):
    """ConfirmPaymentIntent"""
    try:
        confirmation = stripe.PaymentIntent.confirm(
            stripe_id,
            payment_method="pm_card_visa",
            receipt_email=receipt_email,
            return_url='http://localhost:8000' + reverse('posts:all_posts')
        )
    except stripe.error.CardError:
        return reverse('posts:all_posts')
