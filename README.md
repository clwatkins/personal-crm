# Personal CRM app

A lightweight web app to log who you're seeing/meeting/making plans with. Built mainly as an exercise in learning React and docker-compose. This can be productionised on any sort of web hosting service -- I'm using Digital Ocean.

Launched, it should look like this:

![App Interface](interface.png)

## Developer notes

NB: many of the `docker-compose` design patterns come from [this article](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/).

### Launching with `docker-compose`

#### Locally

```shell
sudo docker-compose up --build
sudo docker-compose down -v
```

#### In production

Need to manually seed the database at initial startup as we don't destroy it on restart (for obvious reasons). Don't execute the `create_db` command unless you want to wipe data!

This also expects there to be a `.env.prod` key in the project root directory that mirrors `.env.dev` but with production credentials (and sets `BACKEND_ENV=production`).

```shell
sudo docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
sudo docker-compose exec backend python manage.py create-db
sudo docker-compose exec backend python manage.py seed-db
```

### Manually starting various Docker containers

#### Networking

```shell
sudo docker network create personal-crm-net
```

#### Running Postgres

Note: password is fake, obvs

```shell
sudo docker pull postgres
sudo docker run --name personal-crm-db -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 --net personal-crm-net -it postgres
export SQLALCHEMY_DATABASE_URI=postgresql://postgres:mysecretpassword@localhost:5432/postgres
python manage.py create-db
python manage.py seed-db
```

#### Starting backend

```shell
sudo docker build . -t personal-crm-backend
sudo docker run --rm --name personal-crm-backend -e SQLALCHEMY_DATABASE_URI=postgresql://postgres:mysecretpassword@personal-crm-db:5432/postgres --net personal-crm-net -p 5000:5000 -it personal-crm-backend
```

#### Starting frontend

```shell
npm run start
sudo docker build . -t personal-crm-frontend
sudo docker run --rm --name personal-crm-frontend --net personal-crm-net -p 4000:4000 -it personal-crm-frontend
```

### Running fully manually

#### Frontend

```shell
npm start
```

#### Backend

```shell
poetry shell
SQLALCHEMY_DATABASE_URI=sqlite:///./test.db uvicorn src.main:app --reload --port 5000
```

(and then manually create & seed the database)

## To run a database migration

Follow [Alembic's instructions](https://alembic.sqlalchemy.org/en/latest/)

### Building for Pi

Use Docker's `buildx` tool. Following steps in [this article](https://collabnix.com/building-arm-based-docker-images-on-docker-desktop-made-possible-using-buildx/), commands were something like...

```shell
sudo docker buildx create --name pi-builder --platform linux/arm/v7
sudo docker buildx use pi-builder
sudo docker buildx inspect --bootstrap
sudo docker buildx build backend/Dockerfile --load --tag personal-crm_backend:pi
sudo docker save -o ~/personal-crm-backend-pi.tar personal-crm_backend:pi
# ...and again for frontend image
```

Then you can `scp` the built dockerfiles to Pi to run...

```shell
sudo scp ~/personal-crm-backend-pi.tar pi@raspberrypi.local:/home/pi/personal-crm-backend-pi.tar
sudo docker load -i personal-crm-backend-pi.tar
```
