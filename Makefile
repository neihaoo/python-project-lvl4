.env:
	@cp -n .env.example .env || true

install: .env
	@poetry install

migrate:
	@poetry run python manage.py migrate

transprepare:
	@poetry run django-admin makemessages -l ru

transcompile:
	@poetry run django-admin compilemessages

collectstatic:
	@poetry run python manage.py collectstatic --no-input

setup: install migrate collectstatic

shell:
	@poetry run python manage.py shell

lint:
	@poetry run flake8 .

test:
	@poetry run coverage run manage.py test --parallel

test-coverage-report: test
	@poetry run coverage report -m
	@poetry run coverage erase

test-coverage-report-xml:
	@poetry run coverage xml

start:
	@poetry run python manage.py runserver $(ARGS)

secret_key:
	@poetry run python -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

requirements.txt: poetry.lock
	@poetry export -f requirements.txt -o requirements.txt -E gunicorn

selfcheck:
	@poetry check

check: selfcheck lint test requirements.txt

deploy: check
	git push heroku main

.PHONY: install setup shell lint test check start
