FROM python:3.12-alpine
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONWARNINGS=ignore
ENV PATH="/root/.local/bin:$PATH"
EXPOSE 8000/tcp
WORKDIR /app

RUN apk add --no-cache -v --virtual build-deps \
    make gcc g++ \
    postgresql-dev libpq python3-dev musl-dev \
    libjpeg-turbo-dev zlib-dev libffi-dev cairo-dev libwebp-dev \
    curl

RUN pip install --user poetry==2.2.1

COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-interaction --no-ansi -v \
    && apk del --no-cache build-deps

COPY wait-for /usr/bin/
RUN chmod +x /usr/bin/wait-for

COPY . /app/
RUN chmod +x entrypoint.*
