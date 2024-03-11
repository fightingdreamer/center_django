# center_django

## Install dependencies

```sh
poetry install
```

### Migrate database

```sh
poetry run python manage.py migrate
```

### Run development server with hot-reload

```sh
poetry run serve-dev
```

### Run production server

```sh
poetry run serve-prd
```

### Run production build in container

```sh
podman build --env DJANGO_SECRET=YOUR_SECRET --tag center_django .
podman run --env DJANGO_SECRET=YOUR_SECRET --publish 127.0.0.0:5000:5000/tcp --name center_django center_django
```

or 

```sh
docker build --build-arg DJANGO_SECRET=YOUR_SECRET --tag center_django .
docker run --env DJANGO_SECRET=YOUR_SECRET --publish 127.0.0.0:5000:5000/tcp --name center_django center_django
```

Note: Don't change to `0.0.0.0` aka public internet, this project was creating for exerce purposes and
you generally need some kind of ingress reverse proxy like `caddy` with `https` in front of this container.
