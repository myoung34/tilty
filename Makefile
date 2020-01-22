install:
	if [ ! -d venv ]; then virtualenv venv; fi
	. venv/bin/activate
	pip3 install -r requirements.txt -t dist/ >/dev/null
	rm -rf venv

gen_requirements:
	poetry run pip freeze | grep -Ev 'github.*myoung34.tilty' > requirements.txt

test:
	tox

.PHONY: build test
build:
	docker-compose build

run: build
	docker-compose run tilty
