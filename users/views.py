import secrets
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from config.settings import EMAIL_HOST_USER
from users.forms import ProfileForm, UserForm, UserLogInForm
from users.models import User


class UserLogIn(LoginView):
    """Add stylized form"""

    form_class = UserLogInForm


class UserRegisterView(generic.CreateView):
    """Create user views"""

    model = User
    form_class = UserForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        send_mail(
            subject="Successful registration",
            message="Hello, congratulations on your successful registration",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class ProfileView(generic.UpdateView):
    """Views for updating user's profile"""

    model = User
    form_class = ProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def generate_new_password(request):
    """New  random password generation"""

    data = string.ascii_letters + string.digits + string.punctuation
    new_password = "".join(secrets.choice(data) for _ in range(12))
    request.user.set_password(new_password)
    send_mail(
        subject="New password",
        message=f"Hello, your new password: {new_password}",
        from_email=EMAIL_HOST_USER,
        recipient_list=[request.user.email],
    )
    request.user.save()
    return redirect(reverse("users:login"))
