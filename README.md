# Тестовое задание для ццр

## Управление проектом

 - Склонировать проект: `git clone git@github.com:GoiDcl/test_case_ccr.git`
 - Собрать бэк: `docker-compose -f docker-compose.yml -f docker-compose.override.yml build backend` 
 - Собрать остальные образы: `docker-compose -f docker-compose.yml -f docker-compose.override.yml build` 
 - Поднять проект: `docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d`

### Доступные команды make

 - `make dev_build`:
	Собрать образ для разработки/тестирования

 - `make dev_up`:
	Поднять образ для разработки/тестирования

 - `make dev_up_bg`:
	Поднять образ для разработки/тестирования в фоне

 - `make prod_build`:
	Собрать боевой образ

 - `make prod_up`:
	Поднять боевой образ

 - `make prod_up_bg`:
	Поднять боевой образ в фоне

 - `make down`:
	Отключить образ и удалить контейнеры

 - `make down_volumes`:
	Отключить образ и удалить контейнеры и вольюмы

 - `make exec_backend`:
	Запустить sh в контейнере бэкенда

 - `make shell`:
	Запустить python shell в контейнере бэкенда

 - `make test`:
	Запустить все тесты

 - `make test PATH=*some path*`:
	Запустить все тесты из выбранной директории

## .env
Для работы проекта необходим .env файл (локальная разработка) или переменные окружения в gitlab.
Пример `.env` файла:
```.env
# core
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=my_secret_key

# database
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST_AUTH_METHOD=trust

CELERY_BROKER_URL=redis://redis:6379/0
```

## CI/CD
Подразумевается, что при релизе основная ветка будет изменена с `main` на `master`.\
Написаны джобы для полного цикла автоматического отслеживания и применения изменений для веток `master` и `develop`, включая:
 - линтер (если $SKIP_LINTER = no)
 - запуск тестов pytest (если $RUN_TESTS = yes)
 - запуск тестов миграций (если $RUN_TESTS = yes)
 - откат изменений backend и nginx (для master ветки)

Для тестирования выделены отдельные `.entrypoint.test.sh` и `docker-compose.test.yml`
