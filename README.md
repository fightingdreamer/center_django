# center_django

## Install dependencies

```sh
poetry install
```

### Migrate database

```sh
poetry run python manage.py migrate
```

### Custom Settings

In file `settings.py`:
- LINK_SIZE - minimum length of shortened links
- LINK_RANDOMIZE - use random link padding when set

### Run development server with hot-reload

```sh
poetry run serve-dev
```

### Run production server

```sh
poetry run serve-prd
```

### Run production server as container

```sh
podman build \
    --env DJANGO_SECRET=YOUR_SECRET \
    --tag center_django .

podman run \
    --env DJANGO_SECRET=YOUR_SECRET \
    --publish 127.0.0.1:5000:5000/tcp \
    --name center_django center_django
```

or 

```sh
docker build \
    --build-arg DJANGO_SECRET=YOUR_SECRET \
    --tag center_django .

docker run \
    --env DJANGO_SECRET=YOUR_SECRET \
    --publish 127.0.0.1:5000:5000/tcp \
    --name center_django center_django
```

### Note

Some ditributions configure podman to use more restrictive default bridge,
in case of running both Frontend and Backend in containers, loss of connectivity can be observed.

There are many ways to mitigate this problem, just create a new network and run both containers with it:

```sh
podman network create my_network

podman run \
    --network my_network \
    --env DJANGO_SECRET=YOUR_SECRET \
    --publish 127.0.0.1:5000:5000/tcp \
    --name center_django center_django
```

Proper way to do deployments in Podman requires creating a pod with a port redirection,
that way every container within a pod can reach each other under localhost.
