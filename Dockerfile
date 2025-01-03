FROM python:3.12-slim as base

ARG ENVIRONMENT="production"

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Europe/Moscow \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONPATH="/app/src:$PYTHONPATH" \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.1 \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH" \
    POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    python3-dev \
    libpq-dev \
    build-essential \
    curl \
    git \
    ca-certificates \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - \
    || pip install poetry==$POETRY_VERSION \
    && poetry --version

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry install --only main --no-interaction --no-ansi

COPY ./src /app/src

RUN groupadd -r web && useradd -r -g web web \
    && chown -R web:web /app
USER web

CMD ["poetry", "run", "uvicorn", "tik_tok.main:app", "--host", "0.0.0.0", "--port", "3000"]