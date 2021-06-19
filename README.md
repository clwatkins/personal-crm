# personal-crm

## Docker notes

### Networking

`sudo docker network create personal-crm-net`

### Running postgres

`sudo docker pull postgres`

`sudo docker run --name personal-crm-db -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 --net personal-crm-net -it postgres`

Note: fix password!

`export FLASK_DATABASE_URI=postgresql://postgres:mysecretpassword@localhost:5432/postgres`

`python setup_test_db.py`

### Starting backend

`sudo docker build . -t personal-crm-backend`

`sudo docker run --rm --name personal-crm-backend -e FLASK_DATABASE_URI=postgresql://postgres:mysecretpassword@personal-crm-db:5432/postgres --net personal-crm-net -p 5000:5000 -it personal-crm-backend`

### Starting frontend

`REACT_APP_BACKEND_ADDRESS=http://localhost:5000 npm run start`

`sudo docker build . -t personal-crm-frontend`

`sudo docker run --rm --name personal-crm-frontend -e REACT_APP_BACKEND_ADDRESS=http://personal-crm-backend:5000 --net personal-crm-net -p 4000:4000 -it personal-crm-frontend`
