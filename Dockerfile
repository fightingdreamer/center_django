FROM docker.io/library/alpine:3.19

WORKDIR /opt/app

RUN apk add --no-cache tzdata
RUN apk add --no-cache poetry
RUN apk add --no-cache python3

RUN cp /usr/share/zoneinfo/Europe/Warsaw /etc/localtime
RUN echo "Europe/Warsaw" > /etc/timezone

COPY README.md .
COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install --no-root

COPY manage.py .
COPY center_django center_django
COPY link_shortener link_shortener

RUN poetry install

ENV LC_ALL=C

EXPOSE 5000

RUN ["poetry", "run", "python", "manage.py", "migrate"]
ENTRYPOINT ["poetry", "run", "serve-prd"]
