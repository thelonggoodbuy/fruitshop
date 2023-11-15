run-server-dev:
	python manage.py runserver

run-tasks-dev:
	celery -A config worker -l info

run-schedule-dev:
	celery -A config beat -l info