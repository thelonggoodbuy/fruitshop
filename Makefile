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

run-four_queue-dev:
	celery -A config worker -l info -Q four_queue

run-schedule-dev:
	celery -A config beat -l info

# clear system
docker-total-clean:
	docker-compose -f docker-compose.dev.yml down --volume
	echo y|docker system prune --all
	echo y|docker volume prune --all

dev-up:
	docker-compose -f docker-compose.dev.yml up --build