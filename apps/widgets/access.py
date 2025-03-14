from functools import wraps

from django.shortcuts import get_object_or_404, render

from apps.base.access import login_and_permission_to_access
from apps.dashboards.access import can_access_password_protected_dashboard
from apps.dashboards.models import Dashboard
from apps.projects.access import user_can_access_project
from apps.widgets.models import Widget


def login_and_project_required_or_public_or_in_template(view_func):
    @wraps(view_func)
    def decorator(request, *args, **kwargs):
        widget = Widget.objects.get(pk=kwargs["pk"])
        dashboard = widget.page.dashboard

        if not dashboard or dashboard.project.team.deleted:
            return render(request, "404.html", status=404)

        if dashboard.shared_status == Dashboard.SharedStatus.PUBLIC:
            return view_func(request, *args, **kwargs)

        if (
            dashboard
            and dashboard.shared_status == Dashboard.SharedStatus.PASSWORD_PROTECTED
            and can_access_password_protected_dashboard(request, dashboard)
        ):
            return view_func(request, *args, **kwargs)

        user = request.user
        if not user.is_authenticated:
            return render(request, "404.html", status=404)
        project = widget.page.dashboard.project
        if user_can_access_project(user, project):
            return view_func(request, *args, **kwargs)

        return render(request, "404.html", status=404)

    return decorator


def widget_of_team(user, pk, *args, **kwargs):
    widget = get_object_or_404(Widget, pk=pk)
    return user_can_access_project(user, widget.page.dashboard.project)


login_and_widget_required = login_and_permission_to_access(widget_of_team)
