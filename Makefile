setup:
	poetry install

gen_requirements:
	poetry export --without-hashes -f requirements.txt | grep -vIE '^Warning:' >requirements.txt 2>/dev/null

gen_requirements_dev:
	poetry export --without-hashes --dev -f requirements.txt | grep -vIE '^Warning:' >requirements-dev.txt 2>/dev/null

test:
	poetry run tox

.PHONY: build test
build:
	docker-compose build

run: build
	docker-compose run tilty
