from django.urls import include, path

from . import views

app_name = "widgets"
urlpatterns = [
    path("", views.WidgetList.as_view(), name="list"),
    path("new", views.WidgetCreate.as_view(), name="create"),
    path("<int:pk>", views.WidgetDetail.as_view(), name="detail"),
    path("<int:pk>/update", views.WidgetUpdate.as_view(), name="update"),
    path("<int:pk>/delete", views.WidgetDelete.as_view(), name="delete"),
    path("<int:pk>/config", views.WidgetConfig.as_view(), name="config"),
    path("<int:pk>/output", views.WidgetOutput.as_view(), name="output"),
    path(
        "<int:widget_id>/filters/",
        include(
            "apps.dashboards.widgets.filters.urls",
            namespace="filters",
        ),
    ),
]
