from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from posts.forms import StyleFormMixin
from users.models import User


class UserForm(StyleFormMixin, UserCreationForm):
    """Form for model User"""

    class Meta:
        model = User
        fields = ("phone", "email", "password1", "password2", "subscription")


class ProfileForm(StyleFormMixin, UserChangeForm):
    """Form for user's profile"""

    class Meta:
        model = User
        fields = ("phone", "email", "password", "city", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()
