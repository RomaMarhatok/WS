FROM python:3.13-alpine AS builder

RUN addgroup -S system_user && adduser -S -G system_user user 

WORKDIR /app/_lock

RUN chown -R user:system_user /app/_lock

USER user

COPY --from=ghcr.io/astral-sh/uv:0.10.5 /uv /uvx /bin/

ENV PATH="/root/.local/bin/:$PATH"



COPY pyproject.toml uv.lock  ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

FROM python:3.13-alpine AS dev

WORKDIR /opt

ENV PYTHONDONTWRITEBYTECODE=1

COPY --from=builder /app/_lock/.venv .venv

ENV PATH="/opt/.venv/bin:$PATH"

WORKDIR /ws

COPY . .

EXPOSE 8000