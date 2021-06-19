FROM python:3.9-slim

RUN apt-get update
RUN apt-get install -y make build-essential libpq-dev

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /
RUN poetry install --no-interaction

COPY main.py /code/
WORKDIR /code

ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000
ENV FLASK_DATABASE_URI=sqlite:////test.db
EXPOSE 5000

CMD ["python", "main.py"]