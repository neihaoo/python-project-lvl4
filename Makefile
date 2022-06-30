install:
	poetry install

lint:
	poetry run flake8 task_manager

test:
	poetry run coverage run manage.py test

test-coverage-report: test
	poetry run coverage report -m
	poetry run coverage erase

test-coverage-report-xml:
	poetry run coverage xml

selfcheck:
	poetry check

check: selfcheck lint test 

start:
	poetry run python manage.py runserver 0.0.0.0:8000

secret_key:
	poetry run python -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

requirements.txt:
	poetry export -f requirements.txt -o requirements.txt --extras psycopg2

deploy: check
	git push heroku main

.PHONY: install lint test check requirements.txt deploy
