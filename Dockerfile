FROM docker.io/library/alpine:3.19 AS base
WORKDIR /opt/base

FROM base as build
WORKDIR /opt/app

RUN apk add --no-cache poetry
RUN apk add --no-cache python3

ENV POETRY_VIRTUALENVS_PATH=/root/.poetry/virtualenvs

COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install --no-root

COPY manage.py manage.py
COPY center_django center_django
COPY link_shortener link_shortener
COPY README.md README.md 
RUN poetry install

FROM base as app
WORKDIR /opt/app

RUN apk add --no-cache poetry
RUN apk add --no-cache python3
RUN apk add --no-cache tzdata

RUN cp /usr/share/zoneinfo/Europe/Warsaw /etc/localtime
RUN echo "Europe/Warsaw" > /etc/timezone

ENV POETRY_VIRTUALENVS_PATH=/root/.poetry/virtualenvs

COPY --from=build /root/.poetry /root/.poetry
COPY pyproject.toml .
COPY manage.py manage.py
COPY center_django center_django
COPY link_shortener link_shortener
COPY README.md README.md 

ENV LC_ALL=C

EXPOSE 5000
ENTRYPOINT ["poetry", "run", "serve-prd"]
