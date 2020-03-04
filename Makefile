setup:
	poetry install

gen_requirements:
	poetry export -f requirements.txt >requirements.txt

gen_requirements_dev:
	poetry export --dev -f requirements.txt >requirements-dev.txt

test:
	poetry run tox

.PHONY: build test
build:
	docker-compose build

run: build
	docker-compose run tilty
