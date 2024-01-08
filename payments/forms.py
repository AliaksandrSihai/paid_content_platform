from django import forms

from payments.models import PaymentModel
from posts.forms import StyleFormMixin


class PaymentForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = PaymentModel
        fields = ("subscription",)
