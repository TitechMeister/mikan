from django.conf.urls import url
from registration.views import RegistrationView

urlpatterns = [
    url(r'^', RegistrationView.as_view()),
]
