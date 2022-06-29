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

requirements.txt:
	poetry export -f requirements.txt -o requirements.txt --extras psycopg2

deploy:
	git push heroku main

.PHONY: install lint test selfcheck requirements.txt check
