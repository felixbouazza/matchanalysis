FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /matchanalysis

RUN apt update && apt -y upgrade
RUN apt-get install -y --no-install-recommends curl

COPY poetry.lock pyproject.toml ./

RUN curl -sSL https://install.python-poetry.org | python -
RUN /root/.local/bin/poetry config virtualenvs.create false
RUN /root/.local/bin/poetry install
