#! /usr/bin/env bash
set -x

cd /tfa

# give some time for db to startup
sleep 6

# Run migrations
alembic upgrade head

# start backend
uvicorn app.main:app --host 0.0.0.0 --reload --port 80
