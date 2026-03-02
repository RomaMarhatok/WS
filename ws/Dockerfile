FROM python:3.13-alpine AS builder


WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.10.5 /uv /uvx /bin/

ENV PATH="/root/.local/bin/:$PATH"

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# Copy the project into the intermediate image
COPY . .

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

FROM python:3.13-alpine AS dev

WORKDIR /ws

COPY --from=builder /app/_lock/.venv .venv

ENV PATH="/ws/.venv/bin:$PATH"

EXPOSE 8000