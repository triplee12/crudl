#!/usr/bin/crudl_env bash
coverage erase
coverage run python manage.py test --settings=crudl.settings.test
coverage report
