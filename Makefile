run-server-dev:
	python manage.py runserver

run-tasks-dev:
	celery -A config worker -l info

run-transactions_tasts_queue-dev:
	celery -A config worker -l info -Q trade_transaction_task_queue --concurrency=1

run-second_queue-dev:
	celery -A config worker -l info -Q test_second --concurrency=1

run-auxiliary_tasts_queue-dev:
	celery -A config worker -l info -Q auxiliary_queue --concurrency=1

run-schedule-dev:
	celery -A config beat -l info
