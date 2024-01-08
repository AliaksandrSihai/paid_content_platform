from django.urls import path

from payments.apps import PaymentsConfig
from payments.views import CancelPayment, ConfirmPayment, SuccessPayment

app_name = PaymentsConfig.name

urlpatterns = [
    path("confirm/", ConfirmPayment.as_view(), name="confirm"),
    path("cancel/", CancelPayment.as_view(), name="cancel"),
    path("success/", SuccessPayment.as_view(), name="success"),
]
