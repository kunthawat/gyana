from django.urls import path

from . import views

app_name = "connectors"
urlpatterns = [
    path("", views.ConnectorList.as_view(), name="list"),
    path("new", views.ConnectorCreate.as_view(), name="create"),
    path("<int:pk>", views.ConnectorDetail.as_view(), name="detail"),
    path("<int:pk>/update", views.ConnectorUpdate.as_view(), name="update"),
    path("<int:pk>/delete", views.ConnectorDelete.as_view(), name="delete"),
    path("<int:pk>/authorize", views.ConnectorAuthorize.as_view(), name="authorize"),
    path(
        "<int:pk>/authorize-fivetran",
        views.authorize_fivetran,
        name="authorize-fivetran",
    ),
    path(
        "<int:pk>/authorize-fivetran-redirect",
        views.authorize_fivetran_redirect,
        name="authorize-fivetran-redirect",
    ),
]
