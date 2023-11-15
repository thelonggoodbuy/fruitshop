run-server-dev:
	python manage.py runserver

run-tasks-dev:
	celery -A config worker -l info

run-transactions_tasts-dev:
	celery -A config worker -l info -Q trade_transaction_task_queue

run-second_queue-dev:
	celery -A config worker -l info -Q test_second

run-schedule-dev:
	celery -A config beat -l info
