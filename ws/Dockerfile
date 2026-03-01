FROM python:3.14

WORKDIR /backend

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERCTION=1
RUN echo ls

COPY ./pyproject.toml ./

RUN pip install -U pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

COPY ./ws ./

EXPOSE 5000