dev_build:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml build

dev_up:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up

dev_up_bg:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

prod_build:
	docker-compose -f docker-compose.yml -f docker-compose.production.yml build

prod_up:
	docker-compose -f docker-compose.yml -f docker-compose.production.yml up

prod_up_bg:
	docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d

down:
	docker-compose down

down_volumes:
	docker-compose down -v

exec_backend:
	docker-compose exec backend sh

test:
	docker-compose exec backend pytest

shell:
	docker-compose exec backend python manage.py shell
