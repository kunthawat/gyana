import analytics
import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import View

from apps.base.analytics import ONBOARDING_COMPLETED_EVENT
from apps.base.mixins import PageTitleMixin
from apps.base.views import UpdateView

from .forms import UserNameForm
from .models import CustomUser


class UserOnboarding(PageTitleMixin, UpdateView):
    template_name = "users/onboarding.html"
    model = CustomUser
    form_class = UserNameForm
    page_title = "Onboarding"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self) -> str:
        user = self.request.user

        if user.first_name == "" or user.last_name == "":
            return reverse("users:onboarding")

        analytics.track(self.request.user.id, ONBOARDING_COMPLETED_EVENT)
        return reverse("web:home")


class UserFeedback(View):
    def get(self, request, *args, **kwargs):
        # https://hellonext.co/help/sso-redirects

        encoded_jwt = jwt.encode(
            {
                "email": request.user.email,
                "name": request.user.get_full_name() or request.user.username,
            },
            settings.HELLONEXT_SSO_TOKEN,
            algorithm="HS256",
        )

        url = f"https://app.hellonext.co/redirects/sso?domain={request.GET['domain']}&ssoToken={encoded_jwt}&redirect={request.GET['redirect']}"

        return redirect(url)
