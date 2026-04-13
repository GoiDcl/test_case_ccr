# Тестовое задание для ццр

## Управление проектом

В первую очередь закидываем на сервер файлы проекта.\
Для универсальности можно сбилдить образы локально и закинуть на свой registry,
чтобы образы уже были в наличии.\
Тогда нужно будет заменить в docker-compose файлах
image на правильный путь до образа в registry.\
Пример: `registry.gitlab.my-site.ru/my-project/test_case_hitalent/test_app/backend:${TAG:-latest}`
Когда на сервере есть всё необходимое, поднять проект можно двумя разными способами:

### С помощью make
В корне проекта выполняем:

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

### С помощью стандартных команд *docker-compose*
В корне проекта выполняем:

 - `docker-compose -f docker-compose.yml -f docker-compose.override.yml up`:
	Запуск образа для разработки/тестирования. 
 - `docker-compose -f docker-compose.yml -f docker-compose.override.yml up`:
    Запуск боевого образа. 
 - Для запуска также можно добавить ключи:
   - `backend`, `db`, `redis`, `nginx`: для запуска отдельных контейнеров (вместе с их зависимостями)
   - `-d`: для запуска в фоне
   - `--build`: для сборки перед запуском
 - `docker-compose down`: Отключить образ и удалить контейнеры
 - `docker-compose down -v`: Отключить образ и удалить контейнеры и вольюмы
 - `docker-compose exec backend sh`: Запустить sh в контейнере бэкенда
 - `docker-compose exec backend pytest`: Запустить все тесты
 - `docker-compose exec backend pytest *PATH*`: Запустить все тесты из выбранной директории
 - `docker-compose exec backend python manage.py shell`: Запустить python shell в контейнере бэкенда

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
