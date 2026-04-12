build:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml build

up:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up

redis_up:
	docker-compose up redis

down:
	docker-compose down

exec_backend:
	docker-compose exec backend sh

test:
	docker-compose exec backend pytest

shell:
	docker-compose exec backend python manage.py shell
