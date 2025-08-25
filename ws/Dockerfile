FROM python:3.13-slim

WORKDIR /ws_backend

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERCTION=1

COPY ./pyproject.toml ./
COPY ./README.md ./


RUN pip install -U pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

COPY ./ ./
EXPOSE 5001
RUN find . -print
ENTRYPOINT [ "sh","./ws/entrypoint.sh" ]