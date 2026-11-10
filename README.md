# pingwatch

[![CI](https://github.com/oleksandr-rusyn/pingwatch/actions/workflows/ci.yml/badge.svg)](https://github.com/oleksandr-rusyn/pingwatch/actions/workflows/ci.yml)

Self-hosted website uptime monitor that aims to periodically check your URLs, store response history, calculate uptime and send Telegram alerts when a site goes down.

> 🚧 Work in progress

## What works today
- REST API to create and read monitors
- One-off check run that saves results to PostgreSQL

Not implemented yet: scheduled checks, uptime calculation, Telegram alerts.
The check run still uses a hard-coded URL list, not the monitors from the API.

## Stack
Python 3.14 · FastAPI · SQLAlchemy · Alembic · PostgreSQL · httpx · uv · Docker Compose · pytest · GitHub Actions

## Setup
Requires [uv](https://docs.astral.sh/uv/) and Docker (or Podman) with Compose.

```bash
cp .env.example .env
openssl rand -hex 24
```

Put the generated password in `.env` in both `LOCAL_PG_PASSWORD` and `DATABASE_URL`.
Special characters in the `DATABASE_URL` password must be URL-encoded.

```bash
uv sync
docker compose up -d db
uv run alembic upgrade head
```

## Usage
Run the checks once and save the results:

```bash
uv run pingwatch
```

Start the API, with interactive docs at http://127.0.0.1:8000/docs:

```bash
uv run fastapi dev src/pingwatch/app.py
```

## Tests
```bash
uv run pytest
```
