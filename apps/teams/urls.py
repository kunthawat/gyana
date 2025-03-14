from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from .access import login_and_admin_required, login_and_team_required

app_name = "teams"

membership_urlpatterns = (
    [
        path(
            "",
            login_and_admin_required(views.MembershipList.as_view()),
            name="list",
        ),
        path(
            "<hashid:pk>/update",
            login_and_admin_required(views.MembershipUpdate.as_view()),
            name="update",
        ),
        path(
            "<hashid:pk>/delete",
            login_and_admin_required(views.MembershipDelete.as_view()),
            name="delete",
        ),
    ],
    "team_members",
)

urlpatterns = [
    path("new", login_required(views.TeamCreate.as_view()), name="create"),
    path(
        "<hashid:team_id>",
        login_and_team_required(views.TeamDetail.as_view()),
        name="detail",
    ),
    path(
        "<hashid:team_id>/update",
        login_and_admin_required(views.TeamUpdate.as_view()),
        name="update",
    ),
    path(
        "<hashid:team_id>/delete",
        login_and_admin_required(views.TeamDelete.as_view()),
        name="delete",
    ),
]
