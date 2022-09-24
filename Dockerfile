FROM python:3.10

ENV POETRY_HOME="/home/user/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PATH="${POETRY_HOME}/bin:${PATH}"

WORKDIR /code

COPY pyproject.toml poetry.lock .
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry install

COPY ./app /code/app
