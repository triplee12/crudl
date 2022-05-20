#!/usr/bin/crudl_env bash
DJANGO_SETTINGS_MODULE=portfolio.settings.dev \
DJANGO_SECRET_KEY="change-this-to-50-characters-long-random-string" \
DATABASE_NAME=crudl \
DATABASE_USER=crudl \
DATABASE_PASSWORD="change-this-too" \
PIP_REQUIREMENTS=dev.txt \
docker-compose up --detach --build