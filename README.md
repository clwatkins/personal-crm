# Personal CRM app

A lightweight web app to log who you're seeing/meeting/making plans with. Built mainly as an exercise in learning React and docker-compose. This can be productionised on any sort of web hosting service -- I'm using Digital Ocean.

Launched, it should look like this:

![App Interface](interface.png)

## Developer notes

NB: many of the `docker-compose` design patterns come from https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/.

### Launching with `docker-compose`

#### Locally

```shell
sudo docker-compose up --build
sudo docker-compose down -v
```

#### In production

Need to manually seed the database at initial startup as we don't destroy it on restart (for obvious reasons). Don't execute the `create_db` command unless you want to wipe data!

This also expects there to be a `.env.prod` key in the project root directory that mirrors `.env.dev` but with production credentials (and sets `FLASK_ENV=production`).

```shell
sudo docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
sudo docker-compose exec backend python manage.py create_db
sudo docker-compose exec backend python manage.py seed_db
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
export FLASK_DATABASE_URI=postgresql://postgres:mysecretpassword@localhost:5432/postgres
python manage.py create_db
python manage.py seed_db
```

#### Starting backend

```shell
sudo docker build . -t personal-crm-backend
sudo docker run --rm --name personal-crm-backend -e FLASK_DATABASE_URI=postgresql://postgres:mysecretpassword@personal-crm-db:5432/postgres --net personal-crm-net -p 5000:5000 -it personal-crm-backend
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
export FLASK_DATABASE_URI=sqlite:///./test.db
export FLASK_ENV=development
export FLASK_APP=src/__init__.py
flask run
```

(and then manually create & seed the database)

## To run a database migration

Following https://flask-migrate.readthedocs.io/en/latest/

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```
