# personal-crm

https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/

## With docker-compose

Locally: `sudo docker-compose up --build -d`

`sudo docker-compose down -v`

In production: `sudo docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build`

`sudo docker-compose exec backend python manage.py create_db`

`sudo docker-compose exec backend python manage.py seed_db`

## Manual Docker notes

### Networking

`sudo docker network create personal-crm-net`

### Running postgres

_Note: password is fake, obvs_

`sudo docker pull postgres`

`sudo docker run --name personal-crm-db -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 --net personal-crm-net -it postgres`

`export FLASK_DATABASE_URI=postgresql://postgres:mysecretpassword@localhost:5432/postgres`

`python setup_test_db.py`

### Starting backend

`sudo docker build . -t personal-crm-backend`

`sudo docker run --rm --name personal-crm-backend -e FLASK_DATABASE_URI=postgresql://postgres:mysecretpassword@personal-crm-db:5432/postgres --net personal-crm-net -p 5000:5000 -it personal-crm-backend`

### Starting frontend

`REACT_APP_BACKEND_ADDRESS=http://localhost:5000 npm run start`

`sudo docker build . -t personal-crm-frontend`

`sudo docker run --rm --name personal-crm-frontend -e REACT_APP_BACKEND_ADDRESS=http://personal-crm-backend:5000 --net personal-crm-net -p 4000:4000 -it personal-crm-frontend`

## Running fully manually

### Frontend

`npm start`

### Backend

```bash
poetry shell
export FLASK_DATABASE_URI=sqlite:///./test.db
export FLASK_ENV=development
export FLASK_APP=src/__init__.py
sh local_backend.sh
flask run
```
