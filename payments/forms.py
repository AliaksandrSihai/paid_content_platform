from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxLengthValidator, MaxValueValidator

from posts.forms import StyleFormMixin


class CreditCardNumberField(forms.CharField):
    def clean(self, value):
        value = super().clean(value)
        value = value.replace(" ", "")

        if not value.isdigit():
            raise ValidationError("Only digits are allowed in the card number.")

        formatted_value = " ".join([value[i : i + 4] for i in range(0, len(value), 4)])

        return formatted_value


class PaymentConfirmForm(StyleFormMixin, forms.Form):
    """Form for entering card data"""

    allowed_characters = RegexValidator(
        regex=r"^[a-zA-Z]+\s[a-zA-Z]+$",
        message="Only letters are allowed.",
        code="invalid_name",
    )

    card_number = CreditCardNumberField(
        label="Card Number", required=True, validators=[MaxLengthValidator(16)]
    )
    exp_month = forms.IntegerField(
        label='Expiration Month: "MM"',
        required=True,
        validators=[MaxValueValidator(12)],
    )
    exp_year = forms.IntegerField(
        label='Expiration Year: "YY"', required=True, validators=[MaxValueValidator(30)]
    )
    cvc = forms.IntegerField(
        label="CVC", required=True, validators=[MaxValueValidator(999)]
    )
    name = forms.CharField(
        label='Cardholder Name "Name Surname"',
        required=True,
        validators=[allowed_characters],
    )
