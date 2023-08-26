#! /usr/bin/env bash
set -x

alembic upgrade head

uvicorn main:app \
  --host 0.0.0.0 \
  --reload \
  --port 8000
