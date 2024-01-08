from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views
from users.apps import UsersConfig
from users.views import UserLogIn

app_name = UsersConfig.name


urlpatterns = [
    path("login/", UserLogIn.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout", kwargs={"next_page": "/"}),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("new_password/", views.generate_new_password, name="new_password"),
]
