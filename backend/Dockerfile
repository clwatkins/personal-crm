FROM python:3.9-slim-buster
RUN apt-get update && apt-get install -y netcat build-essential musl-dev libffi-dev libssl-dev cargo libpq-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 5000

WORKDIR /usr/src/app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /usr/src/app/
RUN poetry install --no-interaction

COPY src/ /usr/src/app/src/
COPY entrypoint.sh manage.py /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
