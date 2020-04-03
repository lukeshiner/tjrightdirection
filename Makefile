.PHONY: docs

init:
	poetry install

clear-environment:
	poetry env remove python

re-init:
	make clear-environment
	make init

production-init:
	poetry run pip install --upgrade pip
	poetry install --no-dev

docs:
	cd reference/help && poetry run make html

lock:
	poetry lock

test:
	poetry run python manage.py test
