#!/usr/bin/env bash

cat << EOF

Add to your urls.py:

urlpatterns = [
    ...
    path("{{cookiecutter.app_name}}/", include("apps.{{cookiecutter.app_name}}.urls")),
    ...
]

Update your installed apps in settings.py:

PROJECT_APPS = [
    ...
    "apps.{{cookiecutter.app_name}}",
]

Finally, run your migrations!

EOF