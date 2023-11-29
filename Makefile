run-server-dev:
	python manage.py runserver

run-tasks-dev:
	celery -A config worker -l info

run-transactions_tasts_queue-dev:
	celery -A config worker -l info -Q trade_transaction_task_queue --concurrency=1

run-audit_queue-dev:
	celery -A config worker -l info -Q audit_queue

run-auxiliary_tasts_queue-dev:
	celery -A config worker -l info -Q auxiliary_queue --concurrency=1

run-schedule-dev:
	celery -A config beat -l info

# clear system
dev-docker-total-clean:
	docker-compose -f docker-compose.dev.yml down -v
	echo y|docker system prune --all
	echo y|docker volume prune --all


dev-up-build:
	docker-compose -f docker-compose.dev.yml up --build


dev-up:
	docker-compose -f docker-compose.dev.yml up --build
