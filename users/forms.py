from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from posts.forms import StyleFormMixin
from users.models import User


class UserLogInForm(StyleFormMixin, AuthenticationForm):
    """Stylization AuthenticationForm form"""

    pass


class UserForm(StyleFormMixin, UserCreationForm):
    """Form for model User"""

    class Meta:
        model = User
        fields = ("phone", "email", "password1", "password2")


class ProfileForm(StyleFormMixin, UserChangeForm):
    """Form for user's profile"""

    class Meta:
        model = User
        fields = ("phone", "email", "password", "city", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()
