FROM python:3.13-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:0.10.5 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy\
    UV_NO_DEV=1
    
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the intermediate image
COPY . .

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

FROM python:3.13-alpine AS dev

WORKDIR /ws

COPY --from=builder /app/_lock/.venv .venv


EXPOSE 8000