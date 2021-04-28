from django.urls import path
from rest_framework import routers

from . import views

app_name = "teams"

urlpatterns = [
    path("", views.manage_teams, name="manage_teams"),
    path("list/", views.list_teams, name="list_teams"),
    path("create/", views.create_team, name="create_team"),
    path("<slug:team_slug>/manage/", views.manage_team, name="manage_team"),
    path(
        "<slug:team_slug>/resend-invite/<slug:invitation_id>/",
        views.resend_invitation,
        name="resend_invitation",
    ),
    path(
        "invitation/<slug:invitation_id>/",
        views.accept_invitation,
        name="accept_invitation",
    ),
    path(
        "invitation/<slug:invitation_id>/confirm/",
        views.accept_invitation_confirm,
        name="accept_invitation_confirm",
    ),
]

# drf config
router = routers.DefaultRouter()
router.register("api/teams", views.TeamViewSet)
router.register("api/invitations", views.InvitationViewSet)
urlpatterns += router.urls
