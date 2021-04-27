dev:
    python ./manage.py runserver

celery:
    celery -A superreports_io worker -l info

export:
    poetry export -f requirements.txt --output requirements.txt

format:
    # autoflake --in-place --recursive --remove-all-unused-imports --ignore-init-module-imports .
    black .
    isort .