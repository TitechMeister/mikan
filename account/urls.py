from django.conf.urls import url
from account.views import AccountInfoRetrieveView

urlpatterns = [
    url(r'^', AccountInfoRetrieveView.as_view()),
]
