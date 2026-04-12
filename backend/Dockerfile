FROM python:3.12-slim
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONWARNINGS=ignore
ENV PATH="${PATH}:/root/.local/bin"
EXPOSE 8000/tcp
WORKDIR /app

# Зависимости необходимые для работы
RUN apk add --update --no-cache -v\
    git \
    libpq \
    postgresql-client \
    libjpeg-turbo zlib libffi cairo libwebp \
    postgresql-dev gcc python3-dev musl-dev \
    curl

# Установка пакетов python и зависимостей необходимых для их сборки
RUN apk add --no-cache -v --virtual build-deps \
    make gcc g++ \
    postgresql-dev libpq \
    libjpeg-turbo-dev zlib-dev libffi-dev cairo-dev libwebp-dev

RUN pip install --user poetry==2.2.1

COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-interaction --no-ansi -v \
    && apk del --no-cache build-deps

# Copy wait-for script and give it necessary permissions
COPY wait-for /usr/bin/
RUN chmod +x /usr/bin/wait-for

COPY . /app/
RUN chmod +x entrypoint.*
