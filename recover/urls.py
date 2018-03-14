from django.conf.urls import url
from recover.views import (
    RecoverTokenView,
    VerifyRecoverTokenView,
    RenewPasswordView
)

urlpatterns = [
    url(r'^token/', RecoverTokenView.as_view()),
    url(r'^verify/', VerifyRecoverTokenView.as_view()),
    url(r'^renew/', RenewPasswordView.as_view()),
]
