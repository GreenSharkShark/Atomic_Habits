FROM python:3

RUN pip3 install poetry

WORKDIR /code

COPY ./pyproject.toml poetry.lock

RUN poetry install

COPY . .
